import enum
import http.client

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
                + ", StatusCode=" + str(self.status_code)
                + ", RespHeaders=\"" + str(self.resp_headers) + "\""
                + ", RespBody=\"" + str(self.resp_body) + "\"")

def send_request(url, method, headers, body):
    connection = None
    if Protocol.HTTP == url.protocol:
        connection = http.client.HTTPConnection(host=str(url.domain))
    elif Protocol.HTTPS == url.protocol:
        connection = http.client.HTTPSConnection(host=str(url.domain))
    else:
        raise BackblazeB2Error("Invalid protocol value in URL ("
                               + str(url.protocol) + ")")

    try:
        if Method.GET == method:
            connection.request(method='GET', url=url.to_str_no_proto(),
                               headers=headers)
        elif Method.POST == method:
            connection.request(method='POST', url=url.to_str_no_proto(),
                               headers=headers, body=body)
        else:
            raise BackblazeB2Error("Invalid HTTP method value (" + str(method)
                                   + ")")

        response = connection.getresponse()
        return Response(url, headers, body, response.status,
                        response.getheaders(), response.read())
    except ConnectionResetError as e:
        msg = "Connection error during HTTP request. Url=\"" + str(url) + "\""
        msg += ", method=\"" + str(method) + "\""
        msg += ", req_headers=\"" + str(headers) + "\""
        msg += ", req_body=\"" + str(body) + "\"."
        raise BackblazeB2Error(msg) from e
    finally:
        connection.close()
