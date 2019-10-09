import requests
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

