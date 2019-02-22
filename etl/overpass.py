import logging
from datetime import date

from bonobo.config import Configurable, Option, Service

OVERPASS_URL = 'http://overpass-api.de/api/interpreter'

logger = logging.getLogger(__name__)


class OverpassExtract(Configurable):
    query = Option(str, required=True, positional=True)
    overpass_url = Option(str, required=False, positional=False, default=OVERPASS_URL)

    http = Service('http')

    def __call__(self, http):
        response = http.post(self.overpass_url, data=self.query)

        if not response.ok:
            logger.error(response.text)
            raise RuntimeError('Overpass query fails')

        yield {
            'content': response.content.decode('utf-8'),
            'version': date.today().strftime('%Y.%m.%d')
        }
