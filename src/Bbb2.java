package Bbb2;

import java.net.URI;
import java.net.URISyntaxException;

import Bbb2.Api.RawApi;
import Bbb2.Api.AuthorizeAccountResult;
import com.google.gson.Gson;

public class Bbb2
{
    public static void main(String[] args)
    {
        String json = "{                                                                                        \"absoluteMinimumPartSize\": 5000000,                                                  \"accountId\": \"YOUR_ACCOUNT_ID\",                                                      \"allowed\":                                                                           {                                                                                        \"bucketId\": \"BUCKET_ID\",                                                             \"bucketName\": \"BUCKET_NAME\",                                                         \"capabilities\":                                                                      [                                                                                        \"listBuckets\",                                                                       \"listFiles\",                                                                         \"readFiles\",                                                                         \"shareFiles\",                                                                        \"writeFiles\",                                                                        \"deleteFiles\"                                                                    ],                                                                                   \"namePrefix\": null                                                               },                                                                                   \"apiUrl\": \"https://apiNNN.backblazeb2.com\",                                          \"authorizationToken\": \"4_0022623512fc8f80000000001_0186e431_d18d02_acct_tH7VW03boebOXayIc43-sxptpfA=\",     \"downloadUrl\": \"https://f002.backblazeb2.com\",                                       \"recommendedPartSize\": 100000000                                                 }";

        AuthorizeAccountResult a = new AuthorizeAccountResult(json);









        // RawApi.authorizeAccount("00259d5d420cefb0000000005", "K00223t/RxR6JJ01YlnFvUqud6/v4c4");
    }
}
