package bbb2.util.http;

import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import bbb2.util.http.HttpClientProxy;

public class TestClient implements HttpClientProxy
{
    public TestClient()
    {}

    public HttpResponse<String> send(HttpRequest req) throws HttpException
    {
        return null;
    }
}
