import time
import md5
import hashlib
import hmac

KEY_TIME = "_time"
KEY_AK = "_ak"
PARAMS_SEP = "&"
REQUEST_CHARSET = "UTF-8"

def joinSep(arr_str, sep):
    new_str = ""
    first = True
    for s in arr_str:
        if first:
            first = False
        else:
            new_str = new_str + sep
        new_str = new_str + s
    return new_str

def getSignature(accessKey, secretKey=None, params, time):
    sin = []
    sin.append(KEY_TIME + "=" + str(time)) # May...
    sin.append(KEY_AK + "=" + accessKey)
    if params != None:
        for kk in params:
            sin.append(kk + "=" + params[kk])
    sin.sort()
    paramstring = joinSep(sin, PARAMS_SEP)
    strSign = paramstring + secretKey
    md = md5.new()
    md.update(strSign)
    strSignature = md.hexdigest()
    print "strSignature as: " + strSignature
    return strSignature
    # else:
    #     if body != None:
    #         md = md5.new()
    #         md.update(body)
    #         bodyMD5 = md.hexdigest()
    #     if params != None:
    #         sin = []
    #         for kk in params:
    #             sin.append(kk + "=" + params[kk])
    #         sin.sort()
    #         paramstring = joinSep(sin, PARAMS_SEP)
    #     fmt = time.strftime("%a, %d %m %Y %H:%M:%S CST", time.localtime(time))
    #     strToSign = method.upper() + "\n" + path + "\n" + bodyMD5 + "\n" + fmt + "\n" + paramstring

def gen_sign_v2(sk, method, path, date, params, body):
    sortp = sorted(params.items(), key = lambda d: d[0],reverse = False)
    _key = ["%s=%s" % (k, v) for k, v in sortp]
    _key = "&".join(_key)
    if body:
        _body = hashlib.md5(body).hexdigest()
    _str = method + "\n" + path + "\n" + _body  +"\n" + date + "\n" + _key
    sign = hmac.new(sk, _str, digestmod=hashlib.sha1).hexdigest()
    return sign
