package Bbb2.Api;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.Charset;
import java.nio.charset.IllegalCharsetNameException;
import java.nio.charset.UnsupportedCharsetException;
import java.util.Base64;

import bbb2.api.ApiConnectException;
import bbb2.api.ApiResponseParseException;
import bbb2.api.results.AuthorizeAccountResult;

public class Api
{
    public static AuthorizeAccountResult authorizeAccount(String keyId,
                                                          String appKey)
    throws ApiConnectException, ApiResponseParseException
    {
        String auth = null;
        try
        {
            String key = keyId + ":" + appKey;
            byte[] keyBytes = key.getBytes(Charset.forName("US-ASCII"));
            String keyBase64 = Base64.getEncoder().encodeToString(keyBytes);
            auth = "Basic" + keyBase64;
        }
        catch (UnsupportedCharsetException e)
        {
            e.printStackTrace();
            assert false;
        }
        catch (IllegalCharsetNameException e)
        {
            e.printStackTrace();
            assert false;
        }
        catch (IllegalArgumentException e)
        {
            // ...due to bad charset name.
            e.printStackTrace();
            assert false;
        }

        try
        {
            HttpRequest.Builder reqBuilder = HttpRequest.newBuilder();
            HttpRequest req = reqBuilder.uri(getAuthUrl().toURI())
                                        .GET()
                                        .header("Authorization", auth)
                                        .build();

            HttpClient client = HttpClient.newHttpClient();

            HttpResponse<String> res
            = client.send(req, HttpResponse.BodyHandlers.ofString());

            return new AuthorizeAccountResult(res.body());
        }
        catch (URISyntaxException e)
        {
            e.printStackTrace();
            assert false;
            return null;
        }
        catch (IllegalArgumentException e)
        {
            throw new ApiConnectException(e);
        }
        catch (SecurityException e)
        {
            throw new ApiConnectException(e);
        }
        catch (IOException e)
        {
            throw new ApiConnectException(e);
        }
        catch (InterruptedException e)
        {
            throw new ApiConnectException(e);
        }
    }

    private static URL getAuthUrl()
    {
        try
        {
            String urlString
            = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account";

            return new URL(urlString);
        }
        catch (MalformedURLException e)
        {
            e.printStackTrace();
            assert false;
            return null;
        }
    }
}
