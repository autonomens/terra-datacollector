import bonobo
import requests
from pyfiles.storages import get_storage

from etl.common import HTTPGet
from etl.ckan3 import Ckan3Extract
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


def get_graph(ckan_portal, dataset_id, ressource, namespace, filename):
    graph = bonobo.Graph(
        Ckan3Extract(
            ckan_portal,
            dataset_id,
            ressource
        ),
        HTTPGet(),
        PyfilesLoad(
            namespace,
            filename
        )
    )
    return graph


def main(setting, ckan_portal, dataset_id, ressource, namespace, filename):
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(ckan_portal, dataset_id, ressource, namespace, filename, **options),
            services=get_services(setting, **options)
        )
