import bbb2.api.results.AuthorizeAccountResult;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class Tests
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

        AuthorizeAccountResult result = new AuthorizeAccountResult(test);
        Assertions.assertEquals(result.accountId, "YOUR_ACCOUNT_ID");
        Assertions.assertEquals(result.authToken,
                                "4_0022623512fc8f80000000001_0186e431_d18d02_acct_tH7VW03boebOXayIc43-sxptpfA=");
        Assertions.assertEquals(result.apiUrl.toString(),
                                "https://apiNNN.backblazeb2.com");
        Assertions.assertEquals(result.downloadUrl.toString(),
                                "https://f002.backblazeb2.com");
        Assertions.assertEquals(result.minPartSizeBytes, 5000000);
        Assertions.assertEquals(result.recPartSizeBytes, 100000000);
    }
}
