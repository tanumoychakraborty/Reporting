'''
Created on 3 Jan 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.models import latest_build
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    HOME_PAGE_LATEST_BUILDS_BLOCK, ENV, APP, OPCO, STATUS, TIMESTAMP, BUILD_NO, \
    HOME_PAGE_TITLE
from dashboard.views.basic_template_view import DashboardTemplate


class HomeView(DashboardTemplate):

    def get(self, request):
        
        last_five_report = latest_build.objects.get_last_five_builds()
        
        request.session = {
            'l_f_r' : last_five_report,
            'e_o_m' : self.env_opco_map,
            'p_envs' : self.env_list_fr_saved_pipelines,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'h_p_l_b_b' : HOME_PAGE_LATEST_BUILDS_BLOCK,
            'page_title' : HOME_PAGE_TITLE,
            'env' : ENV,
            'app' : APP,
            'opco' : OPCO,
            'stat' : STATUS,
            'ts' : TIMESTAMP,
            'no' : BUILD_NO,
            }
        template = loader.get_template('dashboard/home.html')           
        return HttpResponse(template.render(request.session, request))
        
