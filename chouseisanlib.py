import requests
import datetime
from bs4 import BeautifulSoup

class Chouseisan(object):
    def _get_token(self):
        url_for_token = 'https://chouseisan.com'
        response = requests.get(url_for_token)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        return soup.find(id='chousei_token').get('value')

    def create_schedule(self, name='No_title', comment='No_comment', kouho='No_option'):
        create_url = 'https://chouseisan.com/schedule/newEvent/create'
        payload = { 'name' : name, 'comment' : comment, 'kouho' : kouho, 'chousei_token' : self._get_token() }
        response = requests.post(create_url, data=payload, allow_redirects=False)

        complete_url = response.headers['location']
        new_schedule_url = 'https://chouseisan.com/s?' + complete_url.split('?')[1]
        return new_schedule_url

    def get_total(self, url, number=3):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find(id='nittei')
        simple_table = []
        table_list = [table for table in tables] # faster than `tables.contents`
        table_list = table_list[1::2] # remove blank line

        for table in table_list:
            row = []
            for t in table:
                if "<class 'bs4.element.Tag'>" == str(type(t)):
                    elements = [e for e in t]
                    row.append(elements[0].string if 1 == len(elements) else elements[1].contents[0].string)
            simple_table.append(row)

        simple_table.pop()
        simple_table.sort(key=lambda l: l.count('○'))
        simple_table.reverse()
        names = simple_table.pop()
        names.pop(0) # remove '日程'

        results = []

        for t in simple_table[0:number]:
            date = t.pop(0)
            result_row = [date]
            for i, e in enumerate(t):
                if '○' == e:
                    result_row.append(names[i])
            results.append(result_row)

        s = ''

        for result in results:
            s += result[0] + '\n'
            s += ' '.join(result[1:]) + '\n\n'

        return s[:-2]

    def _get_days(self, num=7):
        dt_now = datetime.datetime.now()
        result = []
        for i in range(num):
            result.append((dt_now + datetime.timedelta(days = i)).weekday())#.date().isoformat())
        return result

if __name__ == '__main__':
    cho = Chouseisan()
    test = cho._get_days()
    print(test)

