import logging
from datetime import date

from bonobo.config import Configurable, Option, Service

logger = logging.getLogger(__name__)


class HTTPGet(Configurable):
    url = Option(str, required=False, default='url')
    content = Option(str, required=False, default='content')

    http = Service('http')

    def __call__(self, properties, http):
        response = http.get(properties[self.url])
        if not response.ok:
            logger.error(response.text)
            raise RuntimeError(f'Request fails: {properties[self.url]}')
        properties[self.content] = response.content
        yield properties

class ContentWithDateAsVersion(Configurable):
    def __call__(self, content):
        yield {
            'content': content,
            'version': date.today().strftime('%Y.%m.%d')
        }
