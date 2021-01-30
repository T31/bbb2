package bbb2.util.http;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import bbb2.ExitCode;
import bbb2.util.http.HttpClientProxy;

public class RealClient implements HttpClientProxy
{
    public RealClient()
    {
        internalClient = HttpClient.newHttpClient();
    }

    public HttpResponse<String> send(HttpRequest req) throws HttpException
    {
        try
        {
            return internalClient.send(req,
                                       HttpResponse.BodyHandlers.ofString());
        }
        catch (IllegalArgumentException e)
        {
            e.printStackTrace();
            System.exit(ExitCode.PROGRAM_ERROR);
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

    private HttpClient internalClient;
}
