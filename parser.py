import re
import json
from datetime import datetime


# =========================
# SAFE HELPER: CLEAN TOKEN
# =========================
def clean(x):
    if x is None:
        return None
    x = str(x).strip()
    return x if x else None


# =========================
# TIMESTAMP PARSER (ROBUST)
# =========================
def parse_timestamp(ts):
    ts = clean(ts)
    if not ts:
        return None

    # ISO format
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except:
        pass

    # Unix epoch (int or float string)
    try:
        if ts.replace(".", "", 1).isdigit():
            return datetime.fromtimestamp(float(ts))
    except:
        pass

    # 15-Mar-2024 14:23:01
    try:
        return datetime.strptime(ts, "%d-%b-%Y %H:%M:%S")
    except:
        pass

    # 2024/03/15 14:23:01
    try:
        return datetime.strptime(ts, "%Y/%m/%d %H:%M:%S")
    except:
        pass

    return None


# =========================
# RESPONSE TIME PARSER (VERY ROBUST)
# =========================
def parse_response_time(rt):
    rt = clean(rt)
    if not rt or rt == "-":
        return None

    rt = rt.lower()

    try:
        # ms
        if rt.endswith("ms"):
            return float(rt[:-2])

        # seconds
        if rt.endswith("s"):
            return float(rt[:-1]) * 1000

        # raw number (int/float)
        return float(rt)

    except:
        return None


# =========================
# STATUS PARSER (FIX INVALIDS)
# =========================
def parse_status(st):
    st = clean(st)

    if not st or st == "-":
        return None

    try:
        code = int(st)
        if 100 <= code <= 599:
            return code
        return None
    except:
        return None


# =========================
# EXTRACT JSON SAFELY
# =========================
def try_parse_json(line):
    try:
        return json.loads(line)
    except:
        return None


# =========================
# NORMALIZE SPLIT LINE
# =========================
def smart_split(line):
    # handles tabs, multiple spaces, weird spacing
    return re.split(r"[\s\t]+", line)


# =========================
# MAIN PARSER
# =========================
def parse_line(line):
    if not line:
        return None, "empty"

    line = str(line).strip()

    if not line:
        return None, "empty"

    # =========================
    # 1. JSON LOGS
    # =========================
    if line.startswith("{"):
        data = try_parse_json(line)

        if not data:
            return None, "json_malformed"

        return {
            "timestamp": parse_timestamp(data.get("timestamp")),
            "ip": clean(data.get("ip")),
            "method": clean(data.get("method")),
            "path": clean(data.get("path")),
            "status": parse_status(data.get("status")),
            "response_time_ms": parse_response_time(data.get("response_time"))
        }, None

    # =========================
    # 2. NORMAL / BROKEN TEXT LOGS
    # =========================
    parts = smart_split(line)

    # too short → malformed
    if len(parts) < 4:
        return None, "too_few_fields"

    try:
        # SHIFTED / REAL WORLD FIX
        timestamp = parse_timestamp(parts[0])

        # flexible indexing (handles missing shifts)
        ip = clean(parts[1]) if len(parts) > 1 else None
        method = clean(parts[2]) if len(parts) > 2 else None

        # path detection (fallback scan)
        path = None
        status = None
        response_time = None

        for p in parts:
            if p.startswith("/"):
                path = p
            elif p.isdigit() and not status:
                status = parse_status(p)
            elif "ms" in p.lower() or "s" in p.lower() or p.replace(".", "", 1).isdigit():
                response_time = parse_response_time(p)

        return {
            "timestamp": timestamp,
            "ip": ip,
            "method": method,
            "path": path,
            "status": status,
            "response_time_ms": response_time
        }, None

    except Exception:
        return None, "parse_error"