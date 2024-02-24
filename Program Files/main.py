import json
import datetime

from strings import *


def handler(event, context):
    response_text = start_text + help_text

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
            response_text = f"Осталось {delta} дней!"
                
            temp_arr = []
            response_text += "\nОсновной период: "
            for d in main_dates:
                day, mon = d.split(".")
                temp_arr.append(f"{day} {month[mon]}")
            response_text += ", ".join(temp_arr)


            temp_arr = []
            response_text += "\nРезервный период: "
            for d in reserve_dates:
                day, mon = d.split(".")
                temp_arr.append(f"{day} {month[mon]}")
            response_text += ", ".join(temp_arr)
        else:
            if user_input.lower() == "предметы":
                bullit = "• "
                response_text = f"Список предметов:\n{bullit}" +\
                    f"\n{bullit}".join([s.capitalize() for s in dates])
            elif user_input.lower() in ["помощь", "что ты умеешь?", "что ты умеешь"]:
                response_text = help_text
            else:
                response_text = error_text

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': response_text,
            'end_session': 'false'
        },
    }
