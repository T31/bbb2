package bbb2.util.http;

import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import bbb2.util.http.HttpException;

public interface HttpClientProxy
{
    public HttpResponse<String> send(HttpRequest req) throws HttpException;
}
