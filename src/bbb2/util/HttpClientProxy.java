package bbb2.util;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import bbb2.util.HttpException;

// Thinly veiled wrapper around java.net.http.HttpClient. Exists to make unit
// testing feasible.
public class HttpClientProxy
{
    public HttpClientProxy()
    {
        internalClient = HttpClient.newHttpClient();
    }

    public HttpResponse<String> send(HttpRequest req) throws HttpException
    {
        if (!testMode)
        {
            try
            {
                return
                internalClient.send(req, HttpResponse.BodyHandlers.ofString());
            }
            catch (IllegalArgumentException e)
            {
                e.printStackTrace();
                assert false;
                return null;
            }
            catch (InterruptedException e)
            {
                throw new HttpException(e);
            }
            catch (IOException e)
            {
                throw new HttpException(e);
            }
            catch (SecurityException e)
            {
                throw new HttpException(e);
            }
        }
        else
        {
            // Mock up.
            return null;
        }
    }

    public static boolean testMode = false;

    private HttpClient internalClient;
}
