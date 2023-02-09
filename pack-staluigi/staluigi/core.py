from datetime import datetime
import pandas as pd


class Storage:
    """
    Storage class contains all methods to use for data storage
    - CRU(D?) operations
    It is abstract
    """

    def __init__(self, context) -> None:
        # it is using path from context to find different settings
        self.ctx = context

    def write(self, df: pd.DataFrame) -> None:
        # write a Dataframe into storage
        # 1. check (with Catalog) for each df column to be a valid entity
        # 2. open a transaction
        # 3. write each column
        # 3. old different values goes to history
        # 4. close transaction
        pass

    def read(self, names: list) -> pd.DataFrame:
        pass

    def readSnapshot(self, names: list, time: datetime) -> pd.DataFrame:
        pass


class Security:
    """
    Security class contains all methods to use for security
    """

    def __init__(self, context) -> None:
        self.ctx = context
        # TODO: need to get rights (flexible a json or a pickle)
        pass

    def isAllowed(right: str) -> bool:
        pass

class Logging:
    """
    Logging class contains all methods to use for logging
    """

    def __init__(self, context) -> None:
        self.ctx = context
        pass

class Catalog:
    """
    Catalog class contains all methods to use for data structure
    - naming of storage objects and metadata?
    """
    

    def __init__(self, context) -> None:
        self.ctx = context
        pass

    def isValidName(name: str) -> bool:
        # search collections to check if a complete name is valid
        pass

    def getSelection(filter: str) -> list:
        # return a list with all valid names that match filter (regular expression)
        pass

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

