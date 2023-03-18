from collections import defaultdict
from datetime import datetime, timedelta, date
from pprint import pprint


def get_next_week_start(d: datetime.date):
    diff_days = 7 - d.weekday()
    return d + timedelta(days=diff_days)


def prepare_birthday(text: str):
    try:
        bd = datetime.strptime(text, '%d, %m, %Y')
        return bd.replace(year=datetime.now().year).date()
    except ValueError as e:
        print(f"Sorry, date incorrect({e})")


def get_birthdays_per_week(users):
    birthdays = defaultdict(list)

    today = datetime.now().date()

    next_week_start = get_next_week_start(today)
    start_period = next_week_start - timedelta(2)
    end_period = next_week_start + timedelta(4)

    happy_users = [user for user in users if start_period <= prepare_birthday(user['birthday']) <= end_period]

    for user in happy_users:
        current_bd = prepare_birthday(user['birthday'])
        if current_bd.weekday() in (5, 6):
            birthdays['Monday'].append(user['name'])
        else:
            birthdays[current_bd.strftime('%A')].append(user['name'])
    return birthdays


if __name__ == "__main__":

    users = [{"name": "Oleksandr", "birthday": "21, 3, 1991"},
             {"name": "Nina", "birthday": "20, 3, 1972"},
             {"name": "Vova", "birthday": "25, 3, 1991"},
             {"name": "Artem", "birthday": "26, 3, 1991"},
             {"name": "Anna", "birthday": "19, 3, 1996"},
             {"name": "Oleh", "birthday": "18, 3, 1994"},
             {"name": "Maryna", "birthday": "22, 3, 1998"}]

    result = get_birthdays_per_week(users)
    pprint(result)
