package bbb2.api.results;

import java.net.URI;

import bbb2.util.json.JsonObjectProxy;

public class AuthorizeAccountResult
{
    public static class Internals
    {
    }

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
            JsonObjectProxy json = new JsonObjectProxy(jsonString);
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
        }
    }

    public String accountId;
    public String authToken;
    public URI apiUrl;
    public URI downloadUrl;
    public int minPartSizeBytes;
    public int recPartSizeBytes;
}
