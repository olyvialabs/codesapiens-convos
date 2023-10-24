import logging


class Logger(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))

    def get_logs(self):
        return '\n'.join(self.logs)

    def clear_logs(self):
        self.logs.clear()
