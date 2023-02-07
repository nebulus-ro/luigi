from datetime import datetime
from .Context import Context
import pandas as pd

class Storage:
    """
    Storage class contains all methods to use for data storage
    - CRU(D?) operations
    It is abstract
    """
    ctx: Context

    def __init__(self, context: Context) -> None:
        # it is using path from context to find different settings
        ctx = context

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
