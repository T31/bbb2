package bbb2.util.json;

import java.io.StringReader;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReaderFactory;

public class JsonObjectProxy
{
    public JsonObjectProxy(String s)
    {
        internalObj = Json.createReader(new StringReader(s)).readObject();
    }

    public JsonObjectProxy(JsonObject inObj)
    {
        internalObj = inObj;
    }

    public JsonObjectProxy getObject(String key) throws Exception
    {
        JsonObject innerObj = internalObj.getJsonObject(key);
        if (null == innerObj)
        {
            throw new Exception();
        }

        return new JsonObjectProxy(innerObj);
    }

    public String getString(String key)
    {
        try
        {
            return internalObj.getString(key);
        }
        catch (NullPointerException e)
        {
            return "";
        }
        catch (ClassCastException e)
        {
            return "";
        }
    }

    public int getInt(String key)
    {
        try
        {
            return internalObj.getInt(key);
        }
        catch (NullPointerException e)
        {
            return 0;
        }
        catch (ClassCastException e)
        {
            return 0;
        }
    }

    private JsonObject internalObj;
}
