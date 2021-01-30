package bbb2.util.json;

import bbb2.Bbb2Exception;

public class JsonParseException extends Bbb2Exception
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
