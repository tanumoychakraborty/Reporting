'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.models import build_archive
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    HOME_PAGE_LATEST_BUILDS_BLOCK, ENV, APP, OPCO, STATUS, TIMESTAMP, BUILD_NO, \
    BUILD_DETAILS_PAGE_TITLE, BUILD_URL, TOTALC, PASSC, FAILC, IGNOREC, \
    AUTOMATION_REPORT_LINK
from dashboard.views.basic_template_view import DashboardTemplate


class BuildDetail(DashboardTemplate):
    
    def get(self, request, build):
        archive = build_archive.objects.get(build_detail__id=build)

        request.session = {
            'arc' : archive,
            'e_o_m' : self.env_opco_map,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'h_p_l_b_b' : HOME_PAGE_LATEST_BUILDS_BLOCK,
            'page_title' : BUILD_DETAILS_PAGE_TITLE,
            'url' : BUILD_URL,
            'env' : ENV,
            'app' : APP,
            'opco' : OPCO,
            'stat' : STATUS,
            'ts' : TIMESTAMP,
            'no' : BUILD_NO,
            'total' : TOTALC,
            'pass' : PASSC,
            'fail' : FAILC,
            'ignore' : IGNOREC,
            'a_r_l' : AUTOMATION_REPORT_LINK,
            }
        template = loader.get_template('dashboard/build_detail.html')           
        return HttpResponse(template.render(request.session, request))