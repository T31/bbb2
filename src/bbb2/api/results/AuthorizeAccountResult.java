package Bbb2.Api.Results;
import java.net.URI;

public class AuthorizeAccountResult
{
    public AuthorizeAccountResult()
    {}

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
        /*
        try
        {
            JsonObject json = new Gson().fromJson(jsonString, JsonObject.class);
            if (!json.get("accountId"))
            {
                // throw
            }
            accountId = json.get("accountId").getAsString();

            if (!json.get

            System.out.println(json.get("accountId").getAsString());
            System.out.println(json.get("fat").getAsString());
        }
        catch (NullPointerException e)
        {
            System.err.println("Unable to find element");
        }
        */
    }

    public String accountId;
    public String authToken;
    public URI apiUrl;
    public URI downloadUrl;
    public int minPartSizeBytes;
    public int recPartSizeBytes;
}
