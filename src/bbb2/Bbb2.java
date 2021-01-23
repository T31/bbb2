package bbb2;

import java.io.StringReader;
import java.net.URI;
import java.net.URISyntaxException;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReaderFactory;

public class Bbb2
{
    public static void main(String[] args)
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
        
        JsonObject jObject = Json.createReader(new StringReader(test)).readObject();
        System.out.println(jObject.getString("accountId"));
    }
}
