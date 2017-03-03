'''
Created on 20 Feb 2017

@author: tanumoy chakraborty
'''
from requests import Request, Session


SEARCH_SERVER_MONITOR = "dyn/admin/nucleus//atg/search/routing/RoutingSystemService/"
SEARCH_ENGINES = ["ATGReturnOrder", "ATGReturnOrderBulk", "ATGProfile", "ATGProfileBulk", "ATGOrder", "ATGOrderBulk", "indexing environment", "indexing environment - production", "commerce", "indexing environment - staging", "commerce - staging"]
SEARCH_ENGINES_ALIAS = {"ATGReturnOrder":"Return Order", "ATGReturnOrderBulk":"Return Order Bulk", "ATGProfile":"Customer Profile", "ATGProfileBulk":"Customer Profile Bulk", "ATGOrder":"Order", "ATGOrderBulk":"Order Bulk", "indexing environment":"Indexing", \
                        "indexing environment - production":"Production Indexing", "commerce":"Product/Non-Product", "indexing environment - staging":"Staging Indexing", "commerce - staging":"Product/Non-Product Staging"}


def getRoutingSystemServiceUrl(url):
    if url.endswith("/"):
        url = url+SEARCH_SERVER_MONITOR
    else:
        url = url+"/"+SEARCH_SERVER_MONITOR
    return url

def send(url):
    s = Session()
    s.trust_env = False
    req = Request('POST', url)
    prep = req.prepare()
    resp = s.send(prep)
    return resp


def getgetRoutingSystemServiceResponse(url):
    response = send(getRoutingSystemServiceUrl(url))
    response.raise_for_status()
    return response.text

def getSearchEngineDictionary(url):
    r = getgetRoutingSystemServiceResponse(url)
    engines = []
    for e in SEARCH_ENGINES:
        engines.append({"name":SEARCH_ENGINES_ALIAS[e], "desc":getSearchEngineDetail(r, e)})
    return engines
    

def getSearchEngineDetail(desc, engine):
    e_name = ">"+engine+"<"
    d = {}
    frm = desc.find(e_name)
    if frm==-1:
        return None
    desc = desc[frm:]
    d['EnvType'], desc = getTdValue(desc)
    d['ParentProject'], desc = getTdValue(desc)
    d['Index'], desc = getIndexValue(desc)
    d['DeployingIndex'], desc = getTdValue(desc)
    d['HostCount'], desc = getTdValue(desc)
    d['EngineCount'], desc = getTdValue(desc)
    d['RunningEngineCount'], desc = getTdValue(desc)
    return d
    
def getTdValue(s):
    frm = s.find("<td>")
    s = s[frm+4:]
    to = s.find("</td>")
    return s[:to], s[to+5:]

def getIndexValue(s):
    s = s.lstrip()
    if s.startswith('<td><a href='):
        frm = s.find("'>")
        s = s[frm+2:]
        to = s.find("</a>")
        return s[:to], s[to+4:]
    else:
        return getTdValue(s)
    
    
    
    