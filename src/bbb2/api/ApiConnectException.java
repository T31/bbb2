package bbb2.api;

import bbb2.Bbb2Exception;

public class ApiConnectException extends Bbb2Exception
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
