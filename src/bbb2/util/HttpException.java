package bbb2.util;

public class HttpException extends Exception
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
