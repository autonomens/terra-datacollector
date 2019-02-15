import asyncio

import bonobo
import requests
from pyfiles.storages import get_storage

import settings
from etl.common import HTTPGet
from etl.opendatasoft import OpendatasoftExtract
from etl.pyfiles import PyfilesLoad


class Command:
    """ Fetch the file from an OpenData portal under OpenDataSoft and store it into pyfile repository.
    """

    OPENDATASOFT_PORTAL = 'https://data.sncf.com'
    DATASET_ID = 'liste-des-gares'
    FORMAT = 'csv'

    NAMESPACE = 'FR:SNCF'
    FILENAME = 'liste-des-gares.csv'

    def get_services(self, **options):
        pyfile_storage = get_storage(
            settings.PYFILES_BACKEND,
            settings.PYFILES_BACKEND_OPTIONS
        )

        return {
            'pyfile_storage': pyfile_storage,
            'event_loop': asyncio.new_event_loop(),
            'http': requests.Session(),
        }

    def get_graph(self, **options):
        graph = bonobo.Graph()
        graph.add_chain(
           OpendatasoftExtract(
               self.OPENDATASOFT_PORTAL,
               self.DATASET_ID,
               self.FORMAT
           ),
           HTTPGet(),
           PyfilesLoad(
               self.NAMESPACE,
               self.FILENAME,
           )
        )
        return graph


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        cmd = Command()
        bonobo.run(
            cmd.get_graph(**options),
            services=cmd.get_services(**options)
        )
