package mocks;

import java.net.http.HttpClient;
import java.net.http.HttpHeaders;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Optional;
import javax.net.ssl.SSLSession;

import bbb2.api.Api;
import bbb2.util.http.HttpClientProxy;
import bbb2.util.http.HttpException;

public class TestHttpClientProxy implements HttpClientProxy
{
    private class MockResponse<String> implements HttpResponse<String>
    {
        public MockResponse()
        {
        }

        public String body()
        {
            return null;
        }

        public HttpHeaders headers()
        {
            return null;
        }

        public HttpClient.Version version()
        {
            return null;
        }

        public URI uri()
        {
            return null;
        }

        public Optional<SSLSession> sslSession()
        {
            return null;
        }

        public Optional<HttpResponse<String>> previousResponse()
        {
            return null;
        }

        public HttpRequest request()
        {
            return null;
        }

        public int statusCode()
        {
            return 0;
        }
    }

    public HttpResponse<String> send(HttpRequest req) throws HttpException
    {
        try
        {
            if (req.uri() == Api.getAuthUrl().toURI())
            {
                return new MockResponse<String>();
            }
        }
        catch (URISyntaxException e)
        {
            e.printStackTrace();
        }

        return null;
    }
}
