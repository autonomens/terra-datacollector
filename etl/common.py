from bonobo.config import Configurable, Option, Service


class HTTPGet(Configurable):
    url = Option(str, required=False, default='url')
    content = Option(str, required=False, default='content')

    http = Service('http')

    def __call__(self, properties, http):
        response = http.get(properties[self.url])
        if not response.ok:
            logger.error(response.text)
            raise RuntimeError(f'Request fails: {self.url}')
        properties[self.content] = response.text
        yield properties
