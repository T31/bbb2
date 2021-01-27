package bbb2.util.http;

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
