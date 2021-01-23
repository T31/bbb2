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
            Assertions.assertEquals(u.getProtocol(), "https");
            Assertions.assertEquals(u.getHost(), "api.backblazeb2.com");
            Assertions.assertEquals(u.getPath(), "/path");
            Assertions.assertEquals(u.getQuery(), "asdf=33");
            Assertions.assertEquals(u.getRef(), "ref");
        }
        catch (MalformedURLException e)
        {
            e.printStackTrace();
            Assertions.assertEquals(false, true);
        }
    }
}
