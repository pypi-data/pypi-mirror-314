class TempLogLevel:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.original_level = logger.level

    def __enter__(self):
        self.logger.setLevel(self.level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.original_level)