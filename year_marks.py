# -*- coding: utf-8 -*-


from sms_nis import User
from getpass import getpass
from utils import get_actual_year, score_to_mark
from sys import exit


print('Программа используется в целях получния данных с СУШ НИШ Палодара.')
print('Ваши даннные скрипт ни куда не отправляет.')
print('Исходный код: https://github.com/arynyklas/SMS-PVL-NIS/')
print()


login = getpass('Введите Ваш ИИН: ')
password = getpass('Введите Ваш пароль: ')

print()


user = User(login, password)

_login = user.login()


if not _login['success']:
    while _login['success'] != True:
        print('Неправильно введены ИИН/пароль!')
        print()

        if _login['data'] and _login['data'].get('captchaOn'):
            print('Сервис недоступен, попробуйте позже!')
            print('Нажмите ENTER чтобы закрыть программу...')
            getpass('')
            exit(0)

        else:
            login = getpass('Введите Ваш ИИН: ')
            password = getpass('Введите Ваш пароль: ')

        _login = user.login(login, password)

        print()


print('Вход выполнен, данные подгружаются...')
print()

data = {}

year_id = get_actual_year(user.get_school_years())['Id']


for period in user.get_periods(year_id):
    period_id = period['Id']
    parallel_id = user.get_parallels(period_id)[0]['Id']
    klass_id = user.get_klasses(period_id, parallel_id)[0]['Id']
    student_id = user.get_students(period_id, klass_id)[0]['Id']

    user.get_user_diary(period_id, parallel_id, klass_id, student_id)
    subjects_data: list = user.get_subjects()

    for subject in subjects_data:
        if data.get(subject['Name']):
            data[subject['Name']] += subject['Score']
        else:
            data[subject['Name']] = subject['Score']


for name in dict(sorted(data.items())).keys():
    score = round(data[name] / 4, 2)

    if round(score) > 0:
        print('{name} - {mark} ({score}%)'.format(name=name, mark=score_to_mark(score), score=score))


print()
print('Нажмите ENTER чтобы закрыть программу...')
getpass('')
