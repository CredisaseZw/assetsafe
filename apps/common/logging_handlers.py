import logging

class DatabaseAuditHandler(logging.Handler):
    def emit(self, record):
        print(f"[DB AUDIT LOG] {self.format(record)}")
