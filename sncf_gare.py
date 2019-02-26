import bonobo
import requests
from pyfiles.storages import get_storage

import settings
from etl.common import HTTPGet
from etl.opendatasoft import OpendatasoftExtract
from etl.pyfiles import PyfilesLoad

OPENDATASOFT_PORTAL = 'https://data.sncf.com'
DATASET_ID = 'liste-des-gares'
FORMAT = 'csv'

NAMESPACE = 'FR:SNCF'
FILENAME = 'liste-des-gares.csv'


def get_services(**options):
    pyfile_storage = get_storage(
        settings.PYFILES_BACKEND,
        settings.PYFILES_BACKEND_OPTIONS
    )

    return {
        'pyfile_storage': pyfile_storage,
        'http': requests.Session(),
    }


def get_graph(**options):
    graph = bonobo.Graph(
        OpendatasoftExtract(
            OPENDATASOFT_PORTAL,
            DATASET_ID,
            FORMAT
        ),
        HTTPGet(),
        PyfilesLoad(
            NAMESPACE,
            FILENAME,
        )
    )
    return graph


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )
