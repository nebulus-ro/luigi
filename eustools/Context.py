from .Security import Security
from .Catalog import Catalog
from .Logging import Logging
from .Storage import Storage

class Context:
    """
    Context is the class containing instances for other utility classes:
        - Security;
        - Logging;
        - Catalog;
        - Storage.
    This class is a singleton
    """
    security: Security
    catalog: Catalog
    logging: Logging
    storage: Storage
    path: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.logging = Logging(self)
        self.security = Security(self)
        self.catalog = Catalog(self)
        self.storage = Storage(self)
