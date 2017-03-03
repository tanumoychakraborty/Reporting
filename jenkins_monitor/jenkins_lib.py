'''
Created on 5 Jan 2017

@author: tanumoy chakraborty
'''
import ast
import datetime
import os
from requests import Request, Session

from jenkins_monitor.__main__ import logger


legacy_header = {}
cloude_header = {".crumb": "73098caf3ead848305d409e70cd47469", }
cloude_host = "jenkins-master.aws.gha.kfplc.com"
python_api = "api/python/"
fitnesseReport = "fitnesseReport/"
fitnesseScriptDetail = "Details/"
primary_view = "api/python?tree=primaryView[name]"
pipeline_view_info = "api/python?tree=jobs[name,url,color],pipelines[firstJob,pipelines[stages[name,downstreamStages[*]]]]"
job_display_name="api/python?tree=displayName"


def getApiUrl(url):
    if url.endswith("/"):
        url = url + python_api
    else:
        url = url + "/" + python_api
    return url

def getFitnesseReportUrl(url):
    if url.endswith("/"):
        url = url + fitnesseReport
    else:
        url = url + "/" + fitnesseReport
    return url

def getFitnesseScriptDetailUrl(url):
    if url.endswith("/"):
        url = url + fitnesseScriptDetail
    else:
        url = url + "/" + fitnesseScriptDetail
    return url

def getPipelinePrimaryViewUrl(url):
    if url.endswith("/"):
        url = url + primary_view
    else:
        url = url + "/" + primary_view
    return url

def get_fitnesse_page_detail(url):
    return get_page(getFitnesseScriptDetailUrl(url))

    
def get_page(url):
    response = send(url)
    response.raise_for_status()
    return response.text

def get_job_info(url): 
    response = get_resp(getApiUrl(url))
    return ast.literal_eval(response)

def send(url):
    s = Session()
    s.trust_env = False
    req = Request('POST', url)
    prep = req.prepare()
    if cloude_host in url:
        prep.headers['.crumb'] = "73098caf3ead848305d409e70cd47469"
    resp = s.send(prep)
    return resp
    

def get_resp(url):
    response = send(url)
    response.raise_for_status()
    return response.text

def get_job_status(detail):
    if detail["result"] is 'UNSTABLE' or 'SUCCESS':
        return True
    else:
        return False

def get_builds(detail):
    return detail["builds"]

def get_last_successful_build_number(detail):
    return detail["lastSuccessfulBuild"]["number"]

def get_last_successful_build_link(detail):
    return detail["lastSuccessfulBuild"]["url"]

def getPipelinePrimaryView(url):
    response = get_resp(getPipelinePrimaryViewUrl(url))
    return ast.literal_eval(response)

def getViewInfo(url):
    if url.endswith("/"):
        response = get_resp(url + pipeline_view_info)
    else:
        response = get_resp(url + "/" + pipeline_view_info)
    return ast.literal_eval(response)

def getJobDisplayName(url):
    if url.endswith("/"):
        response = get_resp(url+job_display_name)
    else:
        response = get_resp(url + "/" + job_display_name)
    return ast.literal_eval(response)['displayName']
    
    
def get_environment(detail):
    env = ''
    try:
        env = filter(lambda e: 'ENV_PREFIX' in e.values(), filter(lambda a: 'parameters' in a.keys(), detail['actions'])[0]['parameters'])
        return env[0]['value']
    except KeyError:
        logger.info("ENV_PREFIX does not exist")

def getFitnesseBlocks(details):
    blocks = map(lambda x: x['name'], details['children'])
    return blocks

def convert_jenkins_timestamp(timestamp):
    in_seconds = float(timestamp) / 1000
    return datetime.datetime.fromtimestamp(in_seconds)

def formatFitnesseTestDesc(desc):
    frm = desc.find("<link rel=\"stylesheet\"")
    to = desc.find("<table border=\"1\" cellspacing=\"0\"")
    desc = desc[:frm] + desc[to:]
    frm = desc.find("<script src=\"/static/")
    to = desc.find("</body>")
    desc = desc[:frm] + desc[to:]
    desc = replaceAnchor(desc)
    return desc

def replaceAnchor(s):
    f = s.find("<a")
    t = s.find("</a>")
    if t != -1 or f != -1:
        s = s[:f] + s[t + 4:]
        s = replaceAnchor(s)
    return s
