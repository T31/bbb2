import java.net.URL;

import bbb2.api.ApiResponseParseException;
import bbb2.api.results.AuthorizeAccountResult;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class ApiResultsTests
{
    @Test
    void AuthorizeAccountResultTest()
    {
        String test =
        "{" +
        "  \"absoluteMinimumPartSize\": 5000000," +
        "  \"accountId\": \"YOUR_ACCOUNT_ID\"," +
        "  \"allowed\": {" +
        "    \"bucketId\": \"BUCKET_ID\"," +
        "    \"bucketName\": \"BUCKET_NAME\"," +
        "    \"capabilities\": [" +
        "      \"listBuckets\"," +
        "      \"listFiles\"," +
        "      \"readFiles\"," +
        "      \"shareFiles\"," +
        "      \"writeFiles\"," +
        "      \"deleteFiles\"" +
        "    ]," +
        "    \"namePrefix\": null" +
        "  }," +
        "  \"apiUrl\": \"https://apiNNN.backblazeb2.com\"," +
        "  \"authorizationToken\": \"4_0022623512fc8f80000000001_0186e431_d18d02_acct_tH7VW03boebOXayIc43-sxptpfA=\"," +
        "  \"downloadUrl\": \"https://f002.backblazeb2.com\"," +
        "  \"recommendedPartSize\": 100000000" +
        "}";

        try
        {
            AuthorizeAccountResult result = new AuthorizeAccountResult(test);
            Assertions.assertEquals("YOUR_ACCOUNT_ID", result.accountId);
            Assertions.assertEquals("4_0022623512fc8f80000000001_0186e431_d18d02_acct_tH7VW03boebOXayIc43-sxptpfA=",
                                    result.authToken);
            Assertions.assertEquals("https://apiNNN.backblazeb2.com",
                                    result.apiUrl.toString());
            Assertions.assertEquals("https://f002.backblazeb2.com",
                                    result.downloadUrl.toString());
            Assertions.assertEquals(5000000, result.minPartSizeBytes);
            Assertions.assertEquals(100000000, result.recPartSizeBytes);
        }
        catch (ApiResponseParseException e)
        {
            e.printStackTrace();
            Assertions.fail();
        }
    }
}
