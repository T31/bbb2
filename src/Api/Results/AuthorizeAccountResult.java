package Bbb2.Api.Results;

import java.net.URI;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class AuthorizeAccountResult
{
    public AuthorizeAccountResult(String inAccountId, String inAuthToken,
                                  URI inApiUrl, URI inDownloadUrl,
                                  int inMinPartSizeBytes,
                                  int inRecPartSizeBytes)
    {
        accountId = inAccountId;
        authToken = inAuthToken;
        apiUrl = inApiUrl;
        downloadUrl = inDownloadUrl;
        minPartSizeBytes = inMinPartSizeBytes;
        recPartSizeBytes = inRecPartSizeBytes;
    }

    public AuthorizeAccountResult(String json)
    {
        Gson gson = new Gson();
        JsonObject e = gson.fromJson(json, JsonObject.class);
        System.out.println(e.get("accountId").getAsString());
    }

    public String accountId;
    public String authToken;
    public URI apiUrl;
    public URI downloadUrl;
    public int minPartSizeBytes;
    public int recPartSizeBytes;
}
