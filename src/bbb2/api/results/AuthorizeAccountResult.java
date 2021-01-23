package bbb2.api.results;

import java.net.MalformedURLException;
import java.net.URL;

import bbb2.api.ApiParseException;
import bbb2.util.json.JsonObjectProxy;
import bbb2.util.json.JsonParseException;

public class AuthorizeAccountResult
{
    public AuthorizeAccountResult(String jsonString) throws ApiParseException
    {
        try
        {
            JsonObjectProxy json = new JsonObjectProxy(jsonString);
            accountId = json.getString("accountId");
            authToken = json.getString("authorizationToken");
            apiUrl = new URL(json.getString("apiUrl"));
            downloadUrl = new URL(json.getString("downloadUrl"));
            minPartSizeBytes = json.getInt("absoluteMinimumPartSize");
            recPartSizeBytes = json.getInt("recommendedPartSize");
        }
        catch (JsonParseException e)
        {
            throw new ApiParseException("Unable to parse API response.", e);
        }
        catch (MalformedURLException e)
        {
            throw new ApiParseException("Malformed URL in API response.", e);
        }
    }

    public String accountId;
    public String authToken;
    public URL apiUrl;
    public URL downloadUrl;
    public int minPartSizeBytes;
    public int recPartSizeBytes;
}
