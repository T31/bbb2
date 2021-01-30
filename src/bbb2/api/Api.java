package bbb2.api;

import java.io.IOException;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.Charset;
import java.nio.charset.IllegalCharsetNameException;
import java.nio.charset.UnsupportedCharsetException;
import java.util.Base64;

import bbb2.ExitCode;
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
            HttpRequest req = reqBuilder.uri(getAuthUri())
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
            System.exit(ExitCode.PROGRAM_ERROR);
            return null;
        }
        catch (IllegalCharsetNameException e)
        {
            e.printStackTrace();
            System.exit(ExitCode.PROGRAM_ERROR);
            return null;
        }
        catch (IllegalArgumentException e)
        {
            // ...due to bad charset name.
            e.printStackTrace();
            System.exit(ExitCode.PROGRAM_ERROR);
            return null;
        }
        catch (HttpException e)
        {
            throw new ApiConnectException(e);
        }
    }

    public static URI getAuthUri()
    {
        try
        {
            String uriString
            = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account";

            return new URI(uriString);
        }
        catch (URISyntaxException e)
        {
            e.printStackTrace();
            System.exit(ExitCode.PROGRAM_ERROR);
            return null;
        }
    }
}
