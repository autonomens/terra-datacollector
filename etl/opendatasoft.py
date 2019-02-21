import logging

from bonobo.config import Configurable, Option, Service

logger = logging.getLogger(__name__)


class OpendatasoftExtract(Configurable):
    portal = Option(str, required=True, positional=True)
    dataset_id = Option(str, required=True, positional=True)
    format = Option(str, required=True, positional=True)

    http = Service('http')

    def __call__(self, http):
        exports_url, str_date = self.get_metadata(http, self.portal, self.dataset_id)
        version = self.date2version(str_date)
        url = self.get_export_url(http, exports_url, self.format)
        yield {
            'url': url,
            'version': version,
        }

    def get_metadata(self, http, portal, dataset_id):
        url = f'{portal}/api/v2/catalog/datasets/{dataset_id}'
        result = http.get(url)
        if not result.ok:
            raise RuntimeError(f'Fails fetch metedata content from {url}')

        try:
            metadata = result.json()
        except ValueError as e:
            raise ValueError(f'Fails parse json metedata from {url}') from e

        try:
            str_date = metadata['dataset']['metas']['default']['data_processed']
            link = next(filter(lambda d: d['rel'] == 'exports', metadata['links']))
            exports_url = link['href']
        except KeyError as e:
            raise ValueError(f'Fails use metedata from {url}') from e

        return [exports_url, str_date]

    def date2version(self, str_date):
        # ISO date, just cut it
        return str_date[0:10].replace('-', '.')

    def get_export_url(self, http, exports_url, format):
        result = http.get(exports_url)
        if not result.ok:
            raise RuntimeError(f'Fails fetch export list from {exports_url}')

        try:
            exports = result.json()
        except ValueError as e:
            raise ValueError(f'Fails parse json export list from {exports_url}') from e

        try:
            link = next(filter(lambda d: d['rel'] == format, exports['links']))
        except KeyError as e:
            raise ValueError(f'Fails retrive export format {format} from {exports_url}') from e

        if not link:
            raise RuntimeError(f'Export format {format} from {exports_url} not available')

        return link['href']
