from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def days_until_next_birthday(birthdate):
    today = datetime.today()
    next_birthday = datetime(today.year, birthdate.month, birthdate.day)
    if today > next_birthday:
        next_birthday = datetime(today.year + 1, birthdate.month, birthdate.day)
    return (next_birthday - today).days

def get_zodiac_sign(birthdate):
    month, day = birthdate.month, birthdate.day
    zodiac_signs = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 20, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 22, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius")
    ]
    for m, d, sign in zodiac_signs:
        if (month == m and day <= d) or (month == m - 1 and day > d):
            return sign
    return "Capricorn"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        birthdate_str = request.form['birthdate']
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        age = calculate_age(birthdate)
        days_until_birthday = days_until_next_birthday(birthdate)
        zodiac_sign = get_zodiac_sign(birthdate)
        leap_year_status = "Yes" if is_leap_year(birthdate.year) else "No"
        result = {
            'age': age,
            'days_until_birthday': days_until_birthday,
            'zodiac_sign': zodiac_sign,
            'leap_year_status': leap_year_status
        }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
