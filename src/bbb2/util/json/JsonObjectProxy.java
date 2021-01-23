package bbb2.util.json;

import java.io.StringReader;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReaderFactory;

import bbb2.util.json.JsonParseException;

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

    public JsonObjectProxy getObject(String key) throws JsonParseException
    {
        JsonObject innerObj = internalObj.getJsonObject(key);
        if (null == innerObj)
        {
            StringBuilder s = new StringBuilder();
            s.append("Unable to find key \"" + key + "\"");
            s.append(" in response \"" + toString() + "\".");
            throw new JsonParseException(s.toString());
        }

        return new JsonObjectProxy(innerObj);
    }

    public String getString(String key) throws JsonParseException
    {
        try
        {
            return internalObj.getString(key);
        }
        catch (NullPointerException e)
        {
            StringBuilder s = new StringBuilder();
            s.append("Unable to find key \"" + key + "\"");
            s.append(" in response \"" + toString() + "\".");
            throw new JsonParseException(s.toString(), e);
        }
        catch (ClassCastException e)
        {
            StringBuilder s = new StringBuilder();
            s.append("Value type for key \"" + key + "\" was not string.");
            s.append(" Response=\"" + toString() + "\".");
            throw new JsonParseException(s.toString(), e);
        }
    }

    public int getInt(String key) throws JsonParseException
    {
        try
        {
            return internalObj.getInt(key);
        }
        catch (NullPointerException e)
        {
            StringBuilder s = new StringBuilder();
            s.append("Unable to find key \"" + key + "\"");
            s.append(" in response \"" + toString() + "\".");
            throw new JsonParseException(s.toString(), e);
        }
        catch (ClassCastException e)
        {
            StringBuilder s = new StringBuilder();
            s.append("Value type for key \"" + key + "\" was not int.");
            s.append(" Response=\"" + toString() + "\".");
            throw new JsonParseException(s.toString(), e);
        }
    }

    public String toString()
    {
        return internalObj.toString();
    }

    private JsonObject internalObj;
}
