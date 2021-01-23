package bbb2.api;

public class ApiParseException extends Exception
{
    public ApiParseException(String msg)
    {
        super(msg);
    }

    public ApiParseException(String msg, Throwable cause)
    {
        super(msg, cause);
    }
}
