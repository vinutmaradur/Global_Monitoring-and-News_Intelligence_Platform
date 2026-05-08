from datetime import datetime, timedelta
from typing import Optional


# -------------------------------
# 🔹 For News / RSS / GDELT (DateTime)
# -------------------------------
def get_datetime_threshold(time_range: Optional[str]):
    if not time_range:
        return None

    now = datetime.utcnow()

    if time_range == "24h":
        return now - timedelta(hours=24)
    elif time_range == "7d":
        return now - timedelta(days=7)
    elif time_range == "30d":
        return now - timedelta(days=30)

    return None


# -------------------------------
# 🔹 For Earthquake (Unix Timestamp)
# -------------------------------
def get_unix_threshold(time_range: Optional[str], use_millis: bool):
    if not time_range:
        return None

    now = datetime.utcnow()

    if time_range == "24h":
        cutoff = now - timedelta(hours=24)
    elif time_range == "7d":
        cutoff = now - timedelta(days=7)
    elif time_range == "30d":
        cutoff = now - timedelta(days=30)
    else:
        return None

    ts = cutoff.timestamp()

    return int(ts * 1000) if use_millis else int(ts)