from .Context import Context

class Security:
    """
    Security class contains all methods to use for security
    """
    ctx: Context


    def __init__(self, context: Context) -> None:
        self.ctx = context
        # TODO: need to get rights (flexible a json or a pickle)
        pass

    def isAllowed(right: str) -> bool:
        pass