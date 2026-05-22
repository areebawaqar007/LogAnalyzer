import random
from datetime import datetime, timedelta

methods = ["GET", "POST", "DELETE", "PUT"]
paths = ["/api/users", "/api/login", "/api/orders", "/api/products", "/api/profile"]

status_codes = [200, 201, 400, 401, 403, 404, 500, "-"]


# =========================
# TIMESTAMP VARIATIONS
# =========================

def random_time():
    base = datetime(2024, 3, 15)
    delta = timedelta(seconds=random.randint(0, 100000))
    return (base + delta).isoformat() + "Z"


def random_timestamp_variant():
    choice = random.randint(1, 4)

    if choice == 1:
        return random_time()  # ISO
    elif choice == 2:
        return str(random.randint(1700000000, 1800000000))  # epoch
    elif choice == 3:
        return datetime(2024, 3, 15) \
            .strftime("%d-%b-%Y %H:%M:%S")  # 15-Mar-2024
    else:
        return datetime(2024, 3, 15) \
            .strftime("%Y/%m/%d %H:%M:%S")  # 2024/03/15


# =========================
# RESPONSE TIME VARIATIONS
# =========================

def random_response_time():
    choice = random.randint(1, 4)

    if choice == 1:
        return f"{random.randint(50,500)}ms"
    elif choice == 2:
        return f"{round(random.uniform(0.05, 0.9), 3)}s"
    elif choice == 3:
        return str(random.randint(50,500))  # raw number
    elif choice == 4:
        return "-"  # missing


# =========================
# NORMAL LOG
# =========================

def generate_normal_line():
    return f"{random_timestamp_variant()} {random.choice(['192.168.1.'+str(random.randint(1,255))])} {random.choice(methods)} {random.choice(paths)} {random.choice(status_codes)} {random_response_time()}"


# =========================
# JSON LOG FORMAT
# =========================

def generate_json_line():
    return str({
        "timestamp": random_timestamp_variant(),
        "ip": f"10.0.0.{random.randint(1,255)}",
        "method": random.choice(methods),
        "path": random.choice(paths),
        "status": random.choice(status_codes),
        "response_time": random_response_time()
    }).replace("'", '"')


# =========================
# EXTRA FIELDS (REAL WORLD)
# =========================

def generate_extra_fields_line():
    return (
        f"{random_timestamp_variant()} "
        f"192.168.1.{random.randint(1,255)} "
        f"{random.choice(methods)} "
        f"{random.choice(paths)} "
        f"{random.choice(status_codes)} "
        f"{random_response_time()} "
        f"\"Mozilla/5.0 Chrome\" "
        f"referrer:/home"
    )


# =========================
# CORRUPT EDGE CASES
# =========================

def corrupt_line():
    choices = [
        "",  # blank line
        "MALFORMED LINE",
        "2024 broken data !!!",
        "GET /api/users",  # missing fields
        "192.168.1.1 GET POST /api",  # scrambled
        '{"broken": true',  # invalid JSON
        "STACKTRACE ERROR at line 42\nnext line broken",  # multi-line issue
        ":::::::",
        None
    ]
    return random.choice(choices)


def extreme_edge_case():
    choices = [
        "X" * 5000,
        "2024-03-15T12:00:00Z 192.168.1.1 GET /api/用户 200 120ms",
        "2024-03-15T12:00:00Z 192.168.1.1 GET /api -50ms",
        "2029-01-01T00:00:00Z 192.168.1.1 GET /api 200 100ms",
        "2024-03-15T12:00:00Z\t192.168.1.1\tGET\t/api\t200\t100ms",
        "2024-03-15T12:00:00Z GET /api 200 100ms",
        '"{\\"timestamp\\":\\"2024-03-15T12:00:00Z\\",\\"ip\\":\\"1.1.1.1\\"}"',
        "[DEBUG] connection reset by peer",
        "[INFO] service restarted",
        "999 192.168.1.1 GET /api 999 100ms",
        "2024-03-15T12:00:00Z 192.168.1.1 GET /api/😀 200 100ms"
    ]
    return random.choice(choices)
# =========================
# MAIN GENERATOR
# =========================

def main():
    with open("sample_logs.txt", "w", encoding="utf-8") as f:
        for _ in range(1000):

            r = random.random()

            # -------------------------
            # 1. BASIC CORRUPT LINES
            # -------------------------
            if r < 0.08:
                line = corrupt_line()

            # -------------------------
            # 2. EXTREME EDGE CASES
            # -------------------------
            elif r < 0.16:
                line = extreme_edge_case()

            # -------------------------
            # 3. JSON LOG FORMAT
            # -------------------------
            elif r < 0.30:
                line = generate_json_line()

            # -------------------------
            # 4. EXTRA FIELDS / REAL-WORLD LOGS
            # -------------------------
            elif r < 0.45:
                line = generate_extra_fields_line()

            # -------------------------
            # 5. NORMAL LOGS
            # -------------------------
            else:
                line = generate_normal_line()

            # -------------------------
            # SAFETY CHECK
            # -------------------------
            if line is not None:
                f.write(str(line).replace("\n", " ") + "\n")


if __name__ == "__main__":
    main()