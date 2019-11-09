import enum

class Protocol(enum.Enum):
    HTTP = 0
    HTTPS = 1

class Method(enum.Enum):
    GET = 0
    POST = 0

class Domain:
    domain = []

    def __init__(self, domain = []):
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

    def __init__(self, path = []):
        self.path = path

    def __str__(self):
        retVal = "/"
        separator = ""
        for word in self.path:
            retVal += separator + word
            separator = "/"

        return retVal

class Url:
    protocol = Protocol.HTTPS
    domain = Domain()
    path = Path()

    def __init__(self, protocol, domain, path):
        self.protocol = protocol
        self.domain = domain
        self.path = path

    def __str__(self):
        protoString = ""
        if Protocol.HTTP == self.protocol:
            protoString = "http"
        elif Protocol.HTTPS == self.protocol:
            protoString = "https"
        else:
            raise BackblazeB2Error("Invalid protocol enum ("
                                   + str(self.protocol) + ")")

        return protoString + "://" + str(self.domain) + str(self.path)

class Response:
    status_code = None
    resp_headers = None
    resp_body = None

    def __init__(self, status_code, resp_headers, resp_body):
        self.status_code = status_code
        self.resp_headers = resp_headers
        self.resp_body = resp_body

    def __str__(self):
        return ("StatusCode=\"" + str(self.status_code) + "\""
                + ", RespHeaders=\"" + str(self.resp_headers) + "\""
                + ", RespBody=\"" + str(self.resp_body) + "\"")
