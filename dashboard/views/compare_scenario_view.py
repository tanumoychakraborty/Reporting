'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.common.dto_util import createScenarioCompareIntermediateList
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    HOME_PAGE_LATEST_BUILDS_BLOCK, AUTOMATION_REPORT_PAGE_TITLE,COMPARE_IN_LAST_TEXT
from dashboard.views.basic_template_view import DashboardTemplate


class CompareScenario(DashboardTemplate):
    
    def post(self, request):
        test_runs = request.POST.getlist('scenarios[]','')
        __compared__ = map(createScenarioCompareIntermediateList, test_runs)
        compared = filter(None, __compared__)
        request.session = {
            'e_o_m' : self.env_opco_map,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'h_p_l_b_b' : HOME_PAGE_LATEST_BUILDS_BLOCK,
            'page_title' : AUTOMATION_REPORT_PAGE_TITLE,
            'c_i_l_t' : COMPARE_IN_LAST_TEXT,
            'comps' : compared,
            }
        template = loader.get_template('dashboard/scenario_comparison.html')           
        return HttpResponse(template.render(request.session, request))