# -*- coding: utf-8 -*-
import urllib
import urllib.request
import urllib.parse
import time
import json
import random
import hashlib
from collections import OrderedDict
from ssdata_datasource import SS_DATASOURCE

def genParams(_appId,_appSec,reqParams={}):
    m = hashlib.md5()
    timestamp = int(time.time())
    randStr = 'abcdefghijklmnopqrstuvwxyz0123456789'
    _nonceStr = ''.join(random.sample(randStr, 16))
    params = {}
    if len(reqParams)>0:
        for k, v in reqParams.items():
            params[k] = v
    params['app_id'] = _appId
    params['nonce_str'] = _nonceStr
    params['time_stamp'] = str(timestamp)
    params2 = OrderedDict()
    for k in sorted(params):
        params2[k] = params[k]
    _params = ''
    for k, v in params2.items():
        _params += '&' + k + '=' + str(v)
    _params = _params[1:]
    _params += "&app_key=" + _appSec
    m.update(_params.encode(encoding='utf-8'))
    _sign = m.hexdigest()
    params['sign'] = _sign
    return params

def get(url,_appId,_appSec,reqParams={}):
    params = genParams(_appId, _appSec, reqParams)
    data = urllib.parse.urlencode(params)
    print('param data: %s' % data)
    resp = urllib.request.urlopen(url + "?" + data)
    html = resp.read().decode()
    return json.loads(html)

def post(url,_appId,_appSec,reqParams={}):
    params = genParams(_appId, _appSec, reqParams)
    params = urllib.parse.urlencode(params).encode('utf - 8')
    req = urllib.request.Request(url=url,data=params, method='POST')
    response = urllib.request.urlopen(req).read().decode()
    return json.loads(response)

def query(appId,appSec,sql,params=None,datasource=SS_DATASOURCE.DS_EFORM):
    if not type(datasource) is SS_DATASOURCE:
        raise Exception('ERROR:must use enum SS_DATASOURCE!!!!%s' % sql)
    sql = formatSql(sql,params)
    if datasource == SS_DATASOURCE.DS_MACRO:
        str = post('http://wstest.idbhost.com/gw2/api/183',appId,appSec,{'datasource_name':'gjk_macro_deyong_dev','sql':sql})
    elif datasource == SS_DATASOURCE.DS_EFORM:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform', 'sql': sql})
    elif datasource == SS_DATASOURCE.DS_EFORM2:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform2', 'sql': sql})
    elif datasource == SS_DATASOURCE.DS_EFORM_EXT:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform_ext', 'sql': sql})
    elif datasource == SS_DATASOURCE.DS_PRODUCT:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'db_product', 'sql': sql})
    elif datasource == SS_DATASOURCE.DS_DORIS_EFORM:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec,
                   {'datasource_name': 'doris_eform', 'sql': sql})
    elif datasource == SS_DATASOURCE.DS_SDP:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec,
                   {'datasource_name': 'ruoyi_spider', 'sql': sql})
    else:
        raise Exception("unkown datasource:",datasource.name)
    if str.get('ret') and str.get('ret')>10000:
        return str
    if str.get('ret'):
        return str['res']
    else:
        return None

def query_biz(appId,appSec,biz,params=None,datasource=SS_DATASOURCE.DS_EFORM):
    params = json.dumps(params)
    biz = 'biz:' + biz
    if not type(datasource) is SS_DATASOURCE:
        raise Exception('ERROR:must use enum SS_DATASOURCE!!!!%s' % biz)
    if datasource == SS_DATASOURCE.DS_MACRO:
        str = post('http://wstest.idbhost.com/gw2/api/183',appId,appSec,{'datasource_name':'gjk_macro_deyong_dev','sql':biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_EFORM:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform', 'sql': biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_EFORM2:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform2', 'sql': biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_EFORM_EXT:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'gjk_eform_ext', 'sql': biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_PRODUCT:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec, {'datasource_name': 'db_product', 'sql': biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_DORIS_EFORM:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec,
                   {'datasource_name': 'doris_eform', 'sql': biz,'params':params})
    elif datasource == SS_DATASOURCE.DS_SDP:
        str = post('http://wstest.idbhost.com/gw2/api/183', appId, appSec,
                   {'datasource_name': 'ruoyi_spider', 'sql': biz,'params':params})
    else:
        raise Exception("unkown datasource:",datasource.name)
    if str.get('ret') and str.get('ret')>10000:
        return str
    if str.get('ret'):
        return str['res']
    else:
        return None

def sqlone(appId,appSec,sql,params,datasource=SS_DATASOURCE.DS_EFORM):
    sql = 'select * from (' + sql +') ga limit 1'
    return query(appId,appSec,sql,params,datasource=datasource)

def formatSql(sql,params):
    sql = sql.replace('?','%s')
    if not sql.__contains__('%s'):
        return sql
    else:
        return sql%params



