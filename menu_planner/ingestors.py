import requests
from bs4 import BeautifulSoup


class InternetIngestor(object):

    def ingest(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.status = 'failed'
            raise IngestedFailed
        return BeautifulSoup(response.text, 'html.parser')
