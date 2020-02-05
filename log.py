import enum
import os

class Level(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4

    def __str__(self):
        return self.name

def log(level, msg):
    print(str(level) + " : " + str(msg))
    sys.stdout.flush()

def log_info(msg):
    log(Level.INFO, msg)

def log_warning(msg):
    log(Level.WARNING, msg)
