# -*- coding: utf-8 -*-

import time
import md5
import hashlib
import hmac
import urllib,urllib2
import xlrd
import random
import json

KEY_TIME = "_time"
KEY_AK = "_ak"
PARAMS_SEP = "&"
ACCESS_KEY = "superlvr"
SECRET_KEY = "fa034ce350e72d8a3960ba560150cd62"

def getSignature(accessKey, secretKey, params, time):
    sin = []
    sin.append(KEY_TIME + "=" + str(time)) # May...
    sin.append(KEY_AK + "=" + accessKey)
    if params != None:
        for kk in params:
            params_fm = kk + "=" + str(params[kk])
            sin.append(params_fm)
    sin.sort()
    paramstring = joinSep(sin, PARAMS_SEP)
    strSign = paramstring + secretKey
    print "strSign as: " + strSign
    md = md5.new()
    md.update(strSign)
    strSignature = md.hexdigest()
    print "strSignature as: " + strSignature
    return strSignature, paramstring

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

def rdExcel(fileName):
    xl_data = xlrd.open_workbook(fileName)
    sheet_list = xl_data.sheets()
    all_item = []
    for sh in sheet_list:
        if sheet_list.index(sh) < 2:
            continue
        resource,method = '',''
        mine,param = [],{}
        for row in range(sh.nrows): # add necessity logic
            if row == 0:
                continue
            if sh.row_values(row)[0] != '':
                resource,method = sh.row_values(row)[0],sh.row_values(row)[1]
                mine.append(resource)
                mine.append(method)
            name,necessity = sh.row_values(row)[2],sh.row_values(row)[4]
            val = str(sh.row_values(row)[5]).split(',')
            ran_val = random.choice(val)
            param[name] = ran_val
        mine.append(param)
        all_item.append(mine)
    return all_item

# vid:26158328
# type:VOD_2D
# uid:42206040
# token:103ec75801yELWau1m3VlzOQLm1dxKSNCXIc1jpTD8CckagJSsdgeji3HlbjdRhSGm1cN0ljI
# userName:13311225078
# liveId: 2020160810150757 type: VOD_QJ

def testsMain():
    items = rdExcel('APIcase.xlsx')
    for item in items:
        url = item[0]
        method = item[1]
        par = item[2]
        method = method.lower()
        # if "<" and ">" in url:
        #     for i in par.keys():
        #         n_p_k = "<"+str(i)+">"
        #         if n_p_k in url:
        #             url = url.replace(n_p_k, str(par[i]))
        #             par.pop(i)
        # elif "{" and "}" in url:
        #     for i in par.keys():
        #         n_p_k2 = "{"+str(i)+"}"
        #         if n_p_k2 in url:
        #             url = url.replace(n_p_k2, str(par[i]))
        #             par.pop(i)
        if "<" and ">" in url or "{" and "}" in url:
            for i in par.keys():
                n_p_k = "<"+str(i)+">"
                n_p_k2 = "{"+str(i)+"}"
                url = url.replace(n_p_k, str(par[i]))
                url = url.replace(n_p_k2, str(par[i]))
                par.pop(i)
        return_items = getSignature(ACCESS_KEY, SECRET_KEY, par, int(time.time()))
        _sign = return_items[0]
        strpar = return_items[1]
        my_string = strpar + "&_sign=" + _sign
        try:
            if method == "get":
                url2 = url + '?' + my_string
                print "url2 as: " + url2
                response = urllib2.urlopen(url2)
            elif method == "post":
                req = urllib2.Request(url, my_string)
                response = urllib2.urlopen(req)
            elif method == "put": # Not ready
                req = urllib2.Request(url, my_string)
                req.add_header() # To be continue ...
                req.get_method = lambda: 'PUT'
                response = urllib2.urlopen(req)
            elif method == "delete": # Not ready
                req = urllib2.Request(url, my_string)
                req.get_method = lambda: 'DELETE'
                response = urllib2.urlopen(req)
            else:
                print "\t... hehe ..."
            apicontent = response.read()
            j_a_c = json.loads(apicontent)
            print "apicontent as: \n%s\n****************"%(json.dumps(j_a_c,indent=4)).decode("unicode_escape")
        except:
            print "error happend\n****************"

testsMain()