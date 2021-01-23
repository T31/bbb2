package bbb2.api;

public class ApiConnectException extends Exception
{
    public ApiConnectException(String msg)
    {
        super(msg);
    }

    public ApiConnectException(Throwable cause)
    {
        super(cause);
    }

    public ApiConnectException(String msg, Throwable cause)
    {
        super(msg, cause);
    }
}
