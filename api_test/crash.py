import time
import md5
import hashlib
import hmac
import urllib
import urllib2
import json

KEY_TIME = "_time"
KEY_AK = "_ak"
PARAMS_SEP = "&"
REQUEST_CHARSET = "UTF-8"
params = {'userName':'13311225078','userId':'42206040','token':'103ec75801yELWau1m3VlzOQLm1dxKSNCXIc1jpTD8CckagJSsdgeji3HlbjdRhSGm1cN0ljI'}
values = {'time':'2016-8-18 10:12:10',
        'log':1,
        'issue_type':'APP_ANR',
        'source':'autoreport',
        'branch':'s1_stable_011_20160125_p20160206',
        'mac':'84:73:03:c3:b3:08',
        'uptime':'3600',
        'sys_version':'16061310',
        'exception_process':'bbb',
        'description':'aaa'}

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

def getSignature(accessKey, params, time, secretKey):
    sin = []
    sin.append(KEY_TIME + "=" + str(time)) # May...
    sin.append(KEY_AK + "=" + accessKey)
    if params != None:
        for kk in params:
            sin.append(kk + "=" + str(params[kk]))
    sin.sort()
    paramstring = joinSep(sin, PARAMS_SEP)
    strSign = paramstring + secretKey
    #print strSign
    md = md5.new()
    md.update(strSign)
    strSignature = md.hexdigest()
    print "strSignature as: " + strSignature
    return strSignature
    
def getdata():
    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    #time0=time.time()
    res_data = urllib2.urlopen(req)
    #time1=time.time()
    #time4=time1-time0
    #print time4
    res = res_data.read()
    #time2=time.time()
    #time3=time2 - time1
    #print time3
    #jsonStr = json.dumps(res, sort_keys=True, indent=2)
    #print "jsonStr:",jsonStr
    #print jsonStr
    print res
        
time_start=int(time.time())
time_start_str=str(time_start)
sign=getSignature('superlvr',params,1470709738,'fa034ce350e72d8a3960ba560150cd62')
url = "http://vr.scloud.letv.com/api/log/v1/crash?_ak=superlvr&_time="+'1470709738'+"&_sign="+sign
print 'time is:',time_start_str
print 'url is:',url
getdata()
#time_end = int(time.time())
#_time = time_end-time_start
#print _time
