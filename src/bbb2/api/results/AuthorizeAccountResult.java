package bbb2.api.results;

import java.net.URI;

import javax.json.JsonObject;

import bbb2.util.JsonProxy;

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

    public AuthorizeAccountResult(String jsonString)
    {
        try
        {
            JsonObject json = JsonProxy.parse(jsonString);
            accountId = json.getString("accountId");
            authToken = json.getString("authorizationToken");
            apiUrl = new URI(json.getString("apiUrl"));
            downloadUrl = new URI(json.getString("downloadUrl"));
            minPartSizeBytes = json.getInt("absoluteMinimumPartSize");
            recPartSizeBytes = json.getInt("recommendedPartSize");
        }
        catch (Exception e)
        {
            System.err.println(e.toString());
            throw e;
        }
    }

    public String accountId;
    public String authToken;
    public URI apiUrl;
    public URI downloadUrl;
    public int minPartSizeBytes;
    public int recPartSizeBytes;
}
