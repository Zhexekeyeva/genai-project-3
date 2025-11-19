import json
import time
import os

LOG_FILE = "logs.json"
STATS_FILE = "stats.json"


def safe_load_json(path, default):
    """Безопасно загружает JSON, возвращает default если файл пустой или битый."""
    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except Exception:
        return default


def save_log(prompt: str, answer: str, duration: float):
    logs = safe_load_json(LOG_FILE, [])

    logs.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "answer": answer,
        "duration_sec": round(duration, 2),
        "answer_chars": len(answer)
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    update_stats(len(answer))


def update_stats(answer_len: int):
    stats = safe_load_json(STATS_FILE, {
        "total_requests": 0,
        "total_chars": 0
    })

    stats["total_requests"] += 1
    stats["total_chars"] += answer_len

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def get_stats():
    return safe_load_json(STATS_FILE, {
        "total_requests": 0,
        "total_chars": 0
    })