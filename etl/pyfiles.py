import asyncio

from bonobo.config import Configurable, Option, Service
from bonobo.constants import NOT_MODIFIED


class PyfilesLoad(Configurable):
    namespace = Option(str, required=True, positional=True)
    filename = Option(str, required=True, positional=True)
    content = Option(str, required=False, default='content')
    version = Option(str, required=False, default='version')

    pyfile_storage = Service('pyfile_storage')

    def __call__(self, properties, pyfile_storage):
        event_loop = asyncio.new_event_loop()
        event_loop.run_until_complete(pyfile_storage.store(
            stream=properties[self.content],
            namespace=self.namespace,
            filename=self.filename,
            version=properties[self.version]
        ))

        yield NOT_MODIFIED
