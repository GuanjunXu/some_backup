package com.example.apisign;
 
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.SortedSet;
import java.util.TreeSet;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import android.util.Log;
 
public class Signature {
    private static final char HEX_DIGITS[] = "0123456789abcdef".toCharArray();
 
    protected static String toHexString(byte[] b) {
        StringBuilder sb = new StringBuilder(b.length * 2);
        for (int i = 0; i < b.length; i++) {
            sb.append(HEX_DIGITS[(b[i] & 0xf0) >>> 4]);
            sb.append(HEX_DIGITS[b[i] & 0x0f]);
        }
        return sb.toString();
    }
 
    protected static String join(Iterable<String> strings, String sep) {
        StringBuilder sb = new StringBuilder();
        boolean first = true;
        for (String item : strings) {
            if (first)
                first = false;
            else
                sb.append(sep);
            sb.append(item);
        }
        return sb.toString();
    }
 
    public static String sign(String key, String method, String path, byte[] body,
            String date, Map<String, String[]> params) {
        try {
            String bodyMD5 = "";
            if (body != null && body.length != 0) {
                MessageDigest digest;
                digest = MessageDigest.getInstance("MD5");
                digest.update(body);
                bodyMD5 = toHexString(digest.digest());
            }
            String paramString = "";
            if (params != null) {
                SortedSet<String> set = new TreeSet<String>();
                for (String param : params.keySet()) {
                    String[] values = params.get(param);
                    for (String value : values) {
                        set.add(param + "=" + value);
                    }
                }
                paramString = join(set, "&");
            }
            String stringToSign = method + "\n" + path + "\n" + bodyMD5 + "\n" + date + "\n"
                    + paramString;
            Log.i("Sign", stringToSign);
            SecretKeySpec signingKey = new SecretKeySpec(key.getBytes(),
                    "HmacSHA1");
            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(signingKey);
            byte[] rawHmac = mac.doFinal(stringToSign.getBytes());
            return toHexString(rawHmac);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        }
        return "";
    }
}