# vod_stepper/utils.py

import json

def save_report(report_data, path):
    with open(path, 'w') as f:
        json.dump(report_data, f, indent=2)

def format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, min = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}:{min:02}:{sec:02}"
    else:
        return f"{min}:{sec:02}"
