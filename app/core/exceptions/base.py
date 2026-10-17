class AppError(Exception):
    def __init__(self, **kwargs):
        self.extra = kwargs
