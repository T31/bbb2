import enum
import http.client

from BackblazeB2Error import BackblazeB2ConnectError
from BackblazeB2Error import BackblazeB2InternalError

class Protocol(enum.Enum):
    HTTP = 0
    HTTPS = 1

class Method(enum.Enum):
    GET = 0
    POST = 1

class Domain:
    domain = []

    def __init__(self, domain = []):
        self.domain = domain

    def __eq__(self, other):
        if None == other:
            return False

        if len(self.domain) != len(other.domain):
            return False

        for i in range(0, len(self.domain)):
            if self.domain[i] != other.domain[i]:
                return False

        return True

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

    def __eq__(self, other):
        if None == other:
            return False

        if len(self.path) != len(other.path):
            return False

        for i in range(0, len(self.path)):
            if self.path[i] != other.path[i]:
                return False

        return True

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

    def __eq__(self, other):
        if None == other:
            return False

        return ((self.protocol == other.protocol)
                and (self.domain == other.domain)
                and (self.path == other.path))

    def from_string(self, url_string):
        start_idx_inc = 0
        end_idx_ex = url_string.find("://")
        if -1 == end_idx_ex:
            raise BackblazeB2Error("Malformed URL (" + url_string + ").")

        proto_string = url_string[start_idx_inc:end_idx_ex]
        if "http" == proto_string:
            self.protocol = Protocol.HTTP
        elif "https" == proto_string:
            self.protocol = Protocol.HTTPS
        else:
            raise BackblazeB2Error("Malformed URL (" + url_string + ").")

        start_idx_inc = url_string.find("://") + len("://")
        if start_idx_inc >= len(url_string):
            raise BackblazeB2Error("Malformed URL (" + url_string + ").")

        end_idx_ex = url_string.find("/", start_idx_inc)
        if -1 != end_idx_ex:
            domain_list = url_string[start_idx_inc:end_idx_ex].split(".")
            self.domain = Domain(domain_list)
        else:
            self.domain = Domain(url_string[start_idx_inc:].split("."))

        start_idx_inc = end_idx_ex
        if -1 == start_idx_inc:
            self.path = Path([])
        elif (start_idx_inc + len("/")) >= len(url_string):
            self.path = Path([])
        else:
            start_idx_inc += len("/")
            self.path = Path(url_string[start_idx_inc:].split("/"))

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

    def to_str_no_proto(self):
        return str(self.domain) + str(self.path)

class Response:
    req_url = None
    req_headers = None
    req_body = None
    status_code = None
    resp_headers = None
    resp_body = None

    def __init__(self, req_url, req_headers, req_body, status_code,
                 resp_headers, resp_body):
        self.req_url = req_url
        self.req_headers = req_headers
        self.req_body = req_body
        self.status_code = status_code
        self.resp_headers = resp_headers
        self.resp_body = resp_body

    def __str__(self):
        return ("ReqUrl=\"" + str(self.req_url) + "\""
                + ", ReqHeaders=\"" + str(self.req_headers) + "\""
                + ", ReqBody=\"" + str(self.req_body) + "\""
                + ", RespStatusCode=" + str(self.status_code)
                + ", RespHeaders=\"" + str(self.resp_headers) + "\""
                + ", RespBody=\"" + str(self.resp_body) + "\"")

class CachedConnection:
    url = None
    connection = None

    def __init__(self, url, connection):
        self.url = url
        self.connection = connection

    def clear(self):
        if None != self.connection:
            self.connection.close()

        self.connection = None
        self.url = None

cached_connection = CachedConnection(None, None)

def send_request(url, method, headers, body):
    global cached_connection

    if url != cached_connection.url:
        cached_connection.clear()
        cached_connection.url = url

        if Protocol.HTTP == url.protocol:
            cached_connection.connection \
            = http.client.HTTPConnection(host=str(url.domain))
        elif Protocol.HTTPS == url.protocol:
            cached_connection.connection \
            = http.client.HTTPSConnection(host=str(url.domain))
        else:
            raise BackblazeB2InternalError("Invalid protocol value in URL"
                                           + " (" + str(url) + ").")
    try:
        if Method.GET == method:
            cached_connection.connection.request(method='GET', url=str(url),
                                                 headers=headers)
        elif Method.POST == method:
            cached_connection.connection.request(method='POST', url=str(url),
                                                 headers=headers, body=body)
        else:
            raise BackblazeB2InternalError("Invalid HTTP method value"
                                           + " (" + str(method) + ").")

        response = cached_connection.connection.getresponse()
        resp_body = response.read()
        return Response(url, headers, body, response.status,
                        response.getheaders(), resp_body)
    except (http.client.IncompleteRead, BrokenPipeError,
            ConnectionResetError) as e:
        cached_connection.clear()
        msg = "Connection error during HTTP request. Url=\"" + str(url) + "\"" \
              ", method=\"" + str(method) + "\"" \
              ", req_headers=\"" + str(headers) + "\"" \
              ", req_body=\"" + str(body) + "\"."
        raise BackblazeB2ConnectError(msg) from e
