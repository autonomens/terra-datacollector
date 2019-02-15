from bonobo.config import Configurable, Option, Service
from bonobo.constants import NOT_MODIFIED


class PyfilesExtract(Configurable):
    namespace = Option(str, required=True, positional=True)
    filename = Option(str, required=True, positional=True)
    version = Option(str, required=False, positional=True, default='latest')

    pyfile_storage = Service('pyfile_storage')
    event_loop = Service('event_loop')

    def __call__(self, pyfile_storage, event_loop):
        result = event_loop.run_until_complete(
            pyfile_storage.search(
                namespace=self.namespace,
                filename=self.filename,
                version=self.version
            )
        )

        if result is None or 'url' not in result:
            raise RuntimeError(f'Fails extract from pyfiles {self.namespace} {self.filename} {self.version}')
        else:
            yield {
                'url': result['url'],
            }


class PyfilesLoad(Configurable):
    namespace = Option(str, required=True, positional=True)
    filename = Option(str, required=True, positional=True)
    content = Option(str, required=False, default='content')
    version = Option(str, required=False, default='version')

    pyfile_storage = Service('pyfile_storage')
    event_loop = Service('event_loop')

    def __call__(self, properties, pyfile_storage, event_loop):
        event_loop.run_until_complete(pyfile_storage.store(
            stream=properties[self.content],
            namespace=self.namespace,
            filename=self.filename,
            version=properties[self.version]
        ))

        yield NOT_MODIFIED
