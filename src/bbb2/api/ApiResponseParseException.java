package bbb2.api;

public class ApiResponseParseException extends Exception
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
