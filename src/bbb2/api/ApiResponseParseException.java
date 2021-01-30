package bbb2.api;

import bbb2.Bbb2Exception;

public class ApiResponseParseException extends Bbb2Exception
{
    public ApiResponseParseException(String msg)
    {
        super(msg);
    }

    public ApiResponseParseException(Throwable cause)
    {
        super(cause);
    }

    public ApiResponseParseException(String msg, Throwable cause)
    {
        super(msg, cause);
    }
}
