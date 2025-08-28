import datetime
import os

# events: namn -> datum
events = {
    "summer_break": "2026-06-09 15:00",
    "lia_start": "2026-09-25 08:00",
    "christmas": "2026-12-24 00:00",
    "bellas_birthday": "2026-12-07 00:00",
    "new_year": "2026-01-01 00:00",
    "graduation_party": "2026-06-09 16:30"
}

# skapa logs-mapp (om den inte finns)
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "countdown.log")

now = datetime.datetime.now()

with open(log_file, "a") as f:
    for event, date_str in events.items():
        # hantera både med och utan tid i strängen
        if len(date_str.split()) == 1:
            date_str += " 00:00"

        event_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        delta = event_time - now

        if delta.total_seconds() > 0:
            output = f"{event}: {delta.days} days, {delta.seconds//3600} hours, {(delta.seconds//60)%60} minutes left\n"
        else:
            output = f"{event}: already passed!\n"

        print(output.strip())   # visa i terminalen
        f.write(output)         # skriv till loggfilen
