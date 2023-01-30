from .Context import Context

class Catalog:
    """
    Catalog class contains all methods to use for data structure
    - naming of storage objects and metadata?
    """
    ctx: Context


    def __init__(self, context: Context) -> None:
        self.ctx = context
        pass

    def isValidName(name: str) -> bool:
        # search collections to check if a complete name is valid
        pass

    def getSelection(filter: str) -> list:
        # return a list with all valid names that match filter (regular expression)
        pass