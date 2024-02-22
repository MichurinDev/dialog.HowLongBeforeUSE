import json
import datetime

month = {
    "05": "мая",
    "06": "июня"
}

def handler(event, context):
    text = 'Привет! Задаёшься вопросом, сколько осталось до ЕГЭ? Сейчас выясним! По какому предмету хочешь узнать дату?'

    with open("dates.json", encoding="utf-8") as f:
        dates = json.loads(f.read())

    if 'request' in event and 'original_utterance' in event['request'] and len(event['request']['original_utterance']) > 0:
        exam_dates = dates.get(event['request']['original_utterance'].lower(), "Такой предмет отсутствует!")

        if exam_dates != "Такой предмет отсутствует!":
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
            text = "Такой предмет отсутствует!"

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
