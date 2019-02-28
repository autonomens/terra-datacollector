import logging

from bonobo.config import Configurable, Option, Service

logger = logging.getLogger(__name__)


class Ckan3Extract(Configurable):
    portal = Option(str, required=True, positional=True)
    dataset_id = Option(str, required=True, positional=True)
    resource = Option(str, required=True, positional=True)

    http = Service('http')

    def __call__(self, http):
        url, str_date = self.get_metadata(http, self.portal, self.dataset_id)
        version = self.date2version(str_date)
        yield {
            'url': url,
            'version': version,
        }

    def get_metadata(self, http, portal, dataset_id):
        url = f'{portal}/api/3/action/package_show?id={dataset_id}'
        result = http.get(url)
        if not result.ok:
            raise RuntimeError(f'Fails fetch metedata content from {url}')

        try:
            metadata = result.json()
        except ValueError as e:
            raise ValueError(f'Fails parse json metedata from {url}') from e

        try:
            resources = metadata['result']['resources']
            resource = next(filter(lambda r: r['name'] == self.resource, resources))
            exports_url = resource['url']
            str_date = resource['last_modified']
        except KeyError as e:
            raise ValueError(f'Fails use metedata from {url}') from e

        return [exports_url, str_date]

    def date2version(self, str_date):
        # ISO date, just cut it
        return str_date[:10]
