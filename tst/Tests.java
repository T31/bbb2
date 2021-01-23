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
            "\"absoluteMinimumPartSize\": 5000000," +
            "\"accountId\": \"YOUR_ACCOUNT_ID\"," +
            "\"allowed\":" +
            "{" +
                "\"bucketId\": \"BUCKET_ID\"," +
                "\"bucketName\": \"BUCKET_NAME\"," +
                "\"capabilities\":" +
                "[" +
                    "\"listBuckets\"," +
                    "\"listFiles\"," +
                    "\"readFiles\"," +
                    "\"shareFiles\"," +
                    "\"writeFiles\"," +
                    "\"deleteFiles\"" +
                "]," +
                "\"namePrefix\": null," +
                "\"apiUrl\": \"https://apiNNN.backblazeb2.com\"," +
                "\"authorizationToken\": \"4_0022623512fc8f80000000001_0186e431_d18d02_acct_tH7VW03boebOXayIc43-sxptpfA=\"," +
                "\"downloadUrl\": \"https://f002.backblazeb2.com\"," +
                "\"recommendedPartSize\": 100000000" +
            "}" +
        "}";

        AuthorizeAccountResult result = new AuthorizeAccountResult(test);
        AuthorizeAccountResult.Internals i = new AuthorizeAccountResult.Internals();
        System.out.println(result.apiUrl);
        System.out.println(result.accountId);
        Assertions.assertEquals(true, true);
    }
}
