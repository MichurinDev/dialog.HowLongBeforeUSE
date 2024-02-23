import json
import datetime

from strings import *


def handler(event, context):
    text = start_text

    with open("dates.json", encoding="utf-8") as f:
        dates = json.loads(f.read())

    user_input = event['request']['original_utterance']

    if 'request' in event and 'original_utterance' in event['request'] and len(user_input) > 0:
        exam_dates = dates.get(user_input.lower(), error_text)

        if exam_dates != error_text:
            main_dates = exam_dates["main"]
            reserve_dates = exam_dates["reserve"]

            exam_day = datetime.datetime.strptime(main_dates[0], "%d.%m")
            exam_day = datetime.date(year=2024, month=exam_day.month, day=exam_day.day)
            delta = str(exam_day - datetime.date.today()).split()[0]
            text = f"Осталось {delta} дней!"
                
            temp_arr = []
            text += "\nОсновной период: "
            for d in main_dates:
                day, mon = d.split(".")
                temp_arr.append(f"{day} {month[mon]}")
            text += ", ".join(temp_arr)


            temp_arr = []
            text += "\nРезервный период: "
            for d in reserve_dates:
                day, mon = d.split(".")
                temp_arr.append(f"{day} {month[mon]}")
            text += ", ".join(temp_arr)
        else:
            if user_input.lower() == "предметы":
                bullit = "• "
                text = f"Список предметов:\n{bullit}" +\
                    f"\n{bullit}".join([s.capitalize() for s in dates])
            else:
                text = error_text

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
