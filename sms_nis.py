# -*- coding: utf-8 -*-


from requests import Session, Response
from time import time


BASE_URL = 'https://sms.pvl.nis.edu.kz/'


def get_session() -> Session:
    session = Session()
    session.headers['X-Requested-With'] = 'XMLHttpRequest'
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    return session


class User:
    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password
        self._session = get_session()

    def _check(self, response: Response, checker_func=None, checker_func_args=None):
        try:
            json: dict = response.json()

            if json.get('refreshPage'):
                self.login(self._session, self._login, self._password)

                if checker_func:
                    if checker_func_args:
                        checker_func(*checker_func_args)
                    else:
                        checker_func()

                    return False

            return json

        except:
            return response.text

    def _make_request(self, service_method='', method='GET', params=None, data=None, headers=None, json=None, checker_func=None, checker_func_args=None, direct_url=None):
        url = BASE_URL + service_method if not direct_url else direct_url
        response = self._session.request(method, url, params, data, headers, json=json)
        return self._check(response, checker_func, checker_func_args)

    def login(self, login=None, password=None, captcha=None):
        if login:
            self._login = login
        if password:
            self._password = password

        self._session = get_session()
        data = self._make_request(
            'root/Account/LogOn', method='POST',
            headers={
                'Referer': 'https://sms.pvl.nis.edu.kz/Root/Account/Login?ReturnUrl=%2froot'
            },
            json={
                'login': self._login,
                'password': self._password,
                'twoFactorAuthCode': None,
                'captchaInput': captcha,
                'application2FACode': None
            }
        )

        return data

    def get_school_years(self):
        data = self._make_request(
            'Ref/GetSchoolYears', method='POST',
            data={'page': '1', 'start': '0', 'limit': '100'},
            json={'fullData': True, '_dc': int(time())},
            checker_func=self.get_school_years
        )

        if data:
            if not data.get('success'): return False

            datas = data['data']
            return datas

    def get_periods(self, school_year_id):
        data = self._make_request(
            'Ref/GetPeriods', method='POST',
            data={
                'schoolYearId': school_year_id, 'page': '1',
                'start': '0', 'limit': '100'
            },
            json={'_dc': int(time())},
            checker_func=self.get_periods,
            checker_func_args=(school_year_id,)
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_parallels(self, period_id):
        data = self._make_request(
            'JceDiary/GetParallels', method='POST',
            data={
                'periodId': period_id, 'page': '1',
                'start': '0', 'limit': '100'
            },
            json={'_dc': int(time())},
            checker_func=self.get_parallels,
            checker_func_args=(period_id,)
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_klasses(self, period_id, parallel_id):
        data = self._make_request(
            'JceDiary/GetKlasses', method='POST',
            data={
                'periodId': period_id, 'parallelId': parallel_id,
                'page': '1', 'start': '0', 'limit': '100'
            },
            json={'_dc': int(time())},
            checker_func=self.get_klasses,
            checker_func_args=(period_id, parallel_id,)
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_students(self, period_id, klass_id):
        data = self._make_request(
            'JceDiary/GetStudents', method='POST',
            data={
                'periodId': period_id, 'klassId': klass_id,
                'page': '1', 'start': '0', 'limit': '100'
            },
            json={'_dc': int(time())},
            checker_func=self.get_students,
            checker_func_args=(period_id, klass_id,)
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_user_diary(self, period_id, parallel_id, klass_id, student_id):
        data = self._make_request(
            'JceDiary/GetJceDiary', method='POST',
            data={
                'periodId': period_id, 'parallelId': parallel_id,
                'klassId': klass_id, 'studentId': student_id
            },
            checker_func=self.get_user_diary,
            checker_func_args=(period_id, parallel_id, klass_id, student_id,)
        )

        if data:
            if not data.get('success'): return False
            return self._make_request(direct_url=data['data']['Url'])

    def get_subjects(self):
        data = self._make_request(
            'Jce/Diary/GetSubjects', method='POST',
            data={'page': '1', 'start': '0', 'limit': '100'},
            checker_func=self.get_subjects
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_result_by_evaluation(self, journal_id, eval_id):
        data = self._make_request(
            'Jce/Diary/GetResultByEvalution', method='POST',
            data={
                'journalId': journal_id, 'evalId': eval_id,
                'page': '1', 'start': '0', 'limit': '100'
            },
            checker_func=self.get_result_by_evaluation,
            checker_func_args=(journal_id, eval_id,)
        )

        if data:
            if not data.get('success'): return False
            return data['data']

    def get_charts(self):
        data = self._make_request(
            'Home/GetChartData', method='POST',
            data={'page': '1', 'start': '0', 'limit': '100'},
            json={'_dc': int(time())},
            checker_func=self.get_charts
        )

        if data:
            if not data.get('success'): return False
            return data['data']
