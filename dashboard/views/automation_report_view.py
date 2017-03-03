'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.common.dto_util import getEnvOpcoAppFromBuild
from dashboard.models import fitnesse_report
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    HOME_PAGE_LATEST_BUILDS_BLOCK, AUTOMATION_REPORT_PAGE_TITLE, SCENARIO_NAME, \
    STATUS, DURATION, DETAILS_TEXT, COMPARE_TEXT, AUTOMATION_REPORT_LINK
from dashboard.views.basic_template_view import DashboardTemplate


class AutomationReport(DashboardTemplate):
    
    def get(self, request, build):
        report = fitnesse_report.objects.get(build_detail__pk = build)
        aoe = getEnvOpcoAppFromBuild(build)
        test_runs = report.test_run.all()

        request.session = {
            't_r_s' : test_runs,
            'e_o_m' : self.env_opco_map,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'h_p_l_b_b' : HOME_PAGE_LATEST_BUILDS_BLOCK,
            'page_title' : AUTOMATION_REPORT_PAGE_TITLE,
            's_name' : SCENARIO_NAME,
            'status' : STATUS,
            'duration' : DURATION,
            't_c_d' : DETAILS_TEXT,
            'compare' : COMPARE_TEXT,
            'd_a_r' : AUTOMATION_REPORT_LINK,
            'opco' : aoe.app_list.opco,
            'app' : aoe.app_list.app,
            'env' : aoe.env,
            }
        template = loader.get_template('dashboard/detailed_automation_report.html')           
        return HttpResponse(template.render(request.session, request))