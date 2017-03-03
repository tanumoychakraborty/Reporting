'''
Created on 20 Feb 2017

@author: tanumoy chakraborty
'''


from django.http.response import HttpResponse
from django.template import loader
from requests.packages.urllib3.connection import ConnectionError
from requests.packages.urllib3.exceptions import NewConnectionError

from dashboard.models import environment_list, application_host
from dashboard.dynamo_prod_util.common import getSearchEngineDictionary
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    SEARCH_ENGINE_DETAILS_TEXT, STATUS, \
    ENVIRONMENT_DETAILS_PAGE_TITLE, RUNNING_IN, ENGINE_NAME_TEXT, \
    ENVIRONMENT_TYPE_TEXT, PARENT_PROJECT_TEXT, INDEX_TEXT, DEPLOYING_INDEX_TEXT, \
    HOST_COUNT_TEXT, ENGINE_COUNT_TEXT, RUNNING_ENGINE_TEXT, STOPPED_TEXT, \
    NOT_ALL_RUNNING_TEXT, RUNNING_TEXT, NOT_CONFIGUERED_TEXT
from dashboard.views.basic_template_view import DashboardTemplate


class SearchEngines(DashboardTemplate):
    
    def get(self, request, opco, app, env):
        eao = environment_list.objects.get(env = env , app_list__app = app, app_list__opco = opco)
        host = application_host.objects.get(env_opco_app = eao).host
        try:
            detail = getSearchEngineDictionary(host)
        except (ConnectionError, NewConnectionError):
            request.session = {
                'env' : env,
                }
            template = loader.get_template('dashboard/jenkins_connection_timeout.html')           
            return HttpResponse(template.render(request.session, request))            



        request.session = {
            'e_o_m' : self.env_opco_map,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'page_title' : ENVIRONMENT_DETAILS_PAGE_TITLE,
            'env' : env,
            'app' : app,
            'opco' : opco,
            'r_n' : RUNNING_IN,
            'stat' : STATUS,
            'details' : detail,
            's_e_d_t' : SEARCH_ENGINE_DETAILS_TEXT,
            'search_engine' : ENGINE_NAME_TEXT,
            'env_type' : ENVIRONMENT_TYPE_TEXT,
            'p_project' : PARENT_PROJECT_TEXT,
            'index' : INDEX_TEXT,
            'd_index' : DEPLOYING_INDEX_TEXT,
            'h_count' : HOST_COUNT_TEXT,
            'e_count' : ENGINE_COUNT_TEXT,
            'r_engine' : RUNNING_ENGINE_TEXT,
            'stopped' : STOPPED_TEXT,
            'n_a_running' : NOT_ALL_RUNNING_TEXT,
            'running' : RUNNING_TEXT,
            'not_configuered' : NOT_CONFIGUERED_TEXT,
            }
        template = loader.get_template('dashboard/search_engines.html')           
        return HttpResponse(template.render(request.session, request))