import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import bbb2.util.http.HttpClientProxyBuilder;
import mocks.TestHttpClientProxy;

public class ApiProxyTests
{
    @BeforeAll
    public static void setup()
    {
        HttpClientProxyBuilder.mock = new TestHttpClientProxy();
    }

    @Test
    public void authorizeAccountTest()
    {
    }
}
