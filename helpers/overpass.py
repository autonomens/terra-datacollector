import bonobo
import requests
from pyfiles.storages import get_storage

from etl.common import ContentWithDateAsVersion
from etl.overpass import OverpassExtract
from etl.pyfiles import PyfilesLoad


def get_services(settings, **options):
    pyfile_storage = get_storage(
        settings.PYFILES_BACKEND,
        settings.PYFILES_BACKEND_OPTIONS
    )

    return {
        'pyfile_storage': pyfile_storage,
        'http': requests.Session(),
    }


def get_graph(query, namespace, filename, **options):
    graph = bonobo.Graph(
        OverpassExtract(query),
        ContentWithDateAsVersion(),
        PyfilesLoad(namespace, filename)
    )
    return graph


def main(setting, query, namespace, filename):
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(query, namespace, filename, **options),
            services=get_services(setting, **options)
        )
