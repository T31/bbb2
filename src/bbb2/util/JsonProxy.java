package bbb2.util;

import java.io.StringReader;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReaderFactory;

public class JsonProxy
{
    public static JsonObject parse(String s)
    {
        return Json.createReader(new StringReader(s)).readObject();
    }

    public static JsonObject getJsonObject(JsonObject o, String key) throws Exception
    {
        JsonObject j = o.getJsonObject(key);
        if (null == j)
        {
            throw new Exception();
        }

        return j;
    }
}
