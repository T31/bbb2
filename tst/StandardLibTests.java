import java.net.MalformedURLException;
import java.net.URL;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class StandardLibTests
{
    @Test
    void UrlTest()
    {
        try
        {
            URL u = new URL("https://api.backblazeb2.com/path?asdf=33#ref");
            Assertions.assertEquals("https", u.getProtocol());
            Assertions.assertEquals("api.backblazeb2.com", u.getHost());
            Assertions.assertEquals("/path", u.getPath());
            Assertions.assertEquals("asdf=33", u.getQuery());
            Assertions.assertEquals("ref", u.getRef());
        }
        catch (MalformedURLException e)
        {
            e.printStackTrace();
            Assertions.fail();
        }
    }
}
