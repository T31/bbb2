package bbb2.util.http;

import bbb2.util.http.HttpClientProxy;
import bbb2.util.http.RealClient;

public class HttpClientProxyBuilder
{
    public static HttpClientProxy build()
    {
        if (null == mock)
        {
            return new RealClient();
        }

        return mock;
    }

    public static HttpClientProxy mock = null;
}
