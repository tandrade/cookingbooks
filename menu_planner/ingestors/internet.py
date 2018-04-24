
class IngestionFailed(Exception):
    pass

class InternetIngestor(object):

    def __init__(self, url):
        self.url = url
        self.ingested = None
        self.status = 'initialized'

    def ingest(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.status = 'failed'
            raise IngestedFailed
        self.ingested = BeautifulSoup(response.text, 'html.parser')
