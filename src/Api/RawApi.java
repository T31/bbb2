package Bbb2.Api;

import java.nio.charset.Charset;
import java.util.Base64;
import java.net.http.HttpRequest;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpResponse;
import java.io.IOException;

import com.google.gson.Gson;

public class RawApi
{
    public static void authorizeAccount(String keyId, String appKey)
    {
        try
        {
            String key = new String(keyId + ":" + appKey);
            byte[] keyBytes = key.getBytes(Charset.forName("US-ASCII"));
            String keyBase64 = Base64.getEncoder().encodeToString(keyBytes);
            String auth = "Basic" + keyBase64;

            URI auth_uri = new URI("https", "api.backblazeb2.com",
                                   "/b2api/v2/b2_authorize_account", "");

            HttpRequest req = HttpRequest.newBuilder().uri(auth_uri)
                                                      .GET()
                                                      .header("Authorization", auth)
                                                      .build();

            System.out.println("HERE WE GO");

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());

            System.out.println(res.body());
        }
        catch (IllegalArgumentException e)
        {
            System.err.println(e.toString());
        }
        catch (URISyntaxException e)
        {
            System.err.println(e.toString());
        }
        catch (IOException e)
        {
            System.err.println(e.toString());
        }
        catch (InterruptedException e)
        {
            System.err.println(e.toString());
        }
    }
}
