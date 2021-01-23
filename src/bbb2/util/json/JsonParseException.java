package bbb2.util.json;

public class JsonParseException extends Exception
{
    public JsonParseException(String msg)
    {
        super(msg);
    }

    public JsonParseException(Throwable cause)
    {
        super(cause);
    }

    public JsonParseException(String msg, Throwable cause)
    {
        super(msg, cause);
    }
}
