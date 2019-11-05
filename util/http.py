class Domain:
    domain = []

    def __init__(self, domain):
        self.domain = domain

    def __str__(self):
        retVal = ""
        separator = ""
        for word in self.domain:
            retVal += separator + word
            separator = "."

        return retVal

class Path:
    path = []

    def __init__(self, path):
        self.path = path

    def __str__(self):
        retVal = ""
        separator = ""
        for word in self.path:
            retVal += separator + word
            separator = "/"

        return retVal

