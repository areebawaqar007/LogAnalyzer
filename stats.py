from collections import defaultdict
import math


class Stats:
    def __init__(self):
        self.total = 0
        self.valid = 0
        self.malformed = 0

        self.ip_count = defaultdict(int)
        self.endpoint_count = defaultdict(int)

        self.error_4xx = 0
        self.error_5xx = 0

        self.ip_errors = defaultdict(int)
        self.endpoint_errors = defaultdict(int)

        self.endpoint_times = defaultdict(list)

        self.data_quality = {
            "missing_status": 0,
            "missing_response_time": 0,
            "json_lines": 0
        }

    # =========================
    # ADD ENTRY
    # =========================
    def add(self, entry):
        self.total += 1

        if entry is None:
            self.malformed += 1
            return

        self.valid += 1

        ip = entry.get("ip")
        path = entry.get("path")
        status = entry.get("status")
        rt = entry.get("response_time_ms")

        # ---------------- COUNT ----------------
        self.ip_count[ip] += 1
        self.endpoint_count[path] += 1

        # ---------------- ERRORS ----------------
        if status is None:
            self.data_quality["missing_status"] += 1
        elif 400 <= status < 500:
            self.error_4xx += 1
            self.ip_errors[ip] += 1
            self.endpoint_errors[path] += 1
        elif status >= 500:
            self.error_5xx += 1
            self.ip_errors[ip] += 1
            self.endpoint_errors[path] += 1

        # ---------------- RESPONSE TIME ----------------
        if rt is None:
            self.data_quality["missing_response_time"] += 1
        else:
            self.endpoint_times[path].append(rt)

    # =========================
    # PERCENTILE FUNCTION
    # =========================
    def percentile(self, data, p):
        if not data:
            return None
        data = sorted(data)
        k = (len(data) - 1) * (p / 100)
        f = math.floor(k)
        c = math.ceil(k)

        if f == c:
            return data[int(k)]
        return data[f] + (data[c] - data[f]) * (k - f)

    # =========================
    # REPORT
    # =========================
    def report(self):
        print("\n===== LOG ANALYSIS REPORT =====\n")

        # -------- BASIC --------
        print("TOTAL LINES:", self.total)
        print("VALID LINES:", self.valid)
        print("MALFORMED LINES:", self.malformed)

        error_rate = (self.error_4xx + self.error_5xx)
        percent = (error_rate / self.valid * 100) if self.valid else 0

        print("\nERRORS:")
        print("Total Errors:", error_rate)
        print("Error Rate %:", round(percent, 2))
        print("4xx Errors:", self.error_4xx)
        print("5xx Errors:", self.error_5xx)

        # -------- TOP IPS --------
        print("\nTOP IPS:")
        for ip, count in sorted(self.ip_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(ip, "->", count)

        # -------- TOP ENDPOINTS --------
        print("\nTOP ENDPOINTS:")
        for ep, count in sorted(self.endpoint_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(ep, "->", count)

        # -------- FAILURE ENDPOINTS --------
        print("\nMOST ERROR-PRONE ENDPOINTS:")
        for ep, count in sorted(self.endpoint_errors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(ep, "->", count, "errors")

        # -------- FAILURE IPS --------
        print("\nMOST ERROR-PRONE IPS:")
        for ip, count in sorted(self.ip_errors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(ip, "->", count, "errors")

        # -------- LATENCY --------
        print("\nSLOWEST ENDPOINTS (AVG ms):")
        avg = {}
        for ep, times in self.endpoint_times.items():
            if times:
                avg[ep] = sum(times) / len(times)

        for ep, val in sorted(avg.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(ep, "->", round(val, 2), "ms")

        # -------- P95 LATENCY --------
        print("\nP95 LATENCY (ms):")
        for ep, times in self.endpoint_times.items():
            p95 = self.percentile(times, 95)
            if p95:
                print(ep, "->", round(p95, 2))

        # -------- DATA QUALITY --------
        print("\nDATA QUALITY:")
        for k, v in self.data_quality.items():
            print(k.replace("_", " ").title(), ":", v)

        # -------- ALERTS --------
        print("\nALERTS:")

        if percent > 50:
            print("⚠ High system error rate detected!")

        for ep, count in self.endpoint_errors.items():
            if count > 50:
                print(f"⚠ {ep} has high failure count: {count}")

        for ep, times in self.endpoint_times.items():
            if times and sum(times) / len(times) > 300:
                print(f"⚠ {ep} is slow on average")