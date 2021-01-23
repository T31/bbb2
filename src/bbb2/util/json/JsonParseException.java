package bbb2.util.json;

public class JsonParseException extends Exception
{
    public JsonParseException(String s)
    {
        super(s);
    }

    public JsonParseException(String s, Throwable cause)
    {
        super(s, cause);
    }
}
