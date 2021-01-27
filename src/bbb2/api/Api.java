package Bbb2.Api;

import java.io.IOException;
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
import bbb2.util.http.HttpException;
import bbb2.util.http.HttpClientProxy;
import bbb2.util.http.HttpClientProxyBuilder;

public class Api
{
    public static AuthorizeAccountResult authorizeAccount(String keyId,
                                                          String appKey)
    throws ApiConnectException, ApiResponseParseException
    {
        try
        {
            String key = keyId + ":" + appKey;
            byte[] keyBytes = key.getBytes(Charset.forName("US-ASCII"));
            String keyBase64 = Base64.getEncoder().encodeToString(keyBytes);
            String auth = "Basic" + keyBase64;

            HttpRequest.Builder reqBuilder = HttpRequest.newBuilder();
            HttpRequest req = reqBuilder.uri(getAuthUrl().toURI())
                                        .GET()
                                        .header("Authorization", auth)
                                        .build();

            HttpClientProxy client = HttpClientProxyBuilder.build();
            HttpResponse<String> res = client.send(req);

            return new AuthorizeAccountResult(res.body());
        }
        catch (UnsupportedCharsetException e)
        {
            e.printStackTrace();
            assert false;
            return null;
        }
        catch (IllegalCharsetNameException e)
        {
            e.printStackTrace();
            assert false;
            return null;
        }
        catch (IllegalArgumentException e)
        {
            // ...due to bad charset name.
            e.printStackTrace();
            assert false;
            return null;
        }
        catch (URISyntaxException e)
        {
            e.printStackTrace();
            assert false;
            return null;
        }
        catch (HttpException e)
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
