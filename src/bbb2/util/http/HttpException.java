package bbb2.util.http;

import bbb2.Bbb2Exception;

public class HttpException extends Bbb2Exception
{
    public HttpException(String msg)
    {
        super(msg);
    }

    public HttpException(Throwable cause)
    {
        super(cause);
    }

    public HttpException(String msg, Throwable cause)
    {
        super(msg, cause);
    }
}
