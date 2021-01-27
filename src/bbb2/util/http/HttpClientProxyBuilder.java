package bbb2.util.http;

import bbb2.util.http.HttpClientProxy;
import bbb2.util.http.RealClient;
import bbb2.util.http.TestClient;

public class HttpClientProxyBuilder
{
    public static HttpClientProxy build()
    {
        if (testMode)
        {
            return new TestClient();
        }

        return new RealClient();
    }

    public static boolean testMode = false;
}
