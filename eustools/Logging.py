from .Context import Context

class Logging:
    """
    Logging class contains all methods to use for logging
    """
    ctx: Context


    def __init__(self, context: Context) -> None:
        self.ctx = context
        pass