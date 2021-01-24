import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import bbb2.util.HttpClientProxy;

public class ApiTests
{
    @BeforeAll
    public static void setup()
    {
        HttpClientProxy.testMode = true;
    }

    @Test
    public void authorizeAccountTest()
    {
    }
}
