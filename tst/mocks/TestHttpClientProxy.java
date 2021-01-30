package mocks;

import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import bbb2.util.http.HttpClientProxy;
import bbb2.util.http.HttpException;

public class TestHttpClientProxy implements HttpClientProxy
{
    public TestHttpClientProxy()
    {}

    public HttpResponse<String> send(HttpRequest req) throws HttpException
    {
        return null;
    }
}
