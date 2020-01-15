import enum

class Level(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4

    def log_form(self):
        return self.name

def log(level, msg):
    print(level.log_form() + " : " + str(msg))

def log_info(msg):
    log(Level.INFO, msg)

def log_warning(msg):
    log(Level.WARNING, msg)
