'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.models import build_archive, environment_list, build_detail
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    BUILDS_ARCHIVE_PAGE_APP_INFO, STATUS, BUILDS_LIST_PAGE_TITLE, ENV, APP, OPCO, TIMESTAMP, \
    BUILD_NO, RUNNING_IN
from dashboard.views.basic_template_view import DashboardTemplate


class BuildsArchive(DashboardTemplate):
    
    def get(self, request, opco, app, env):
        eao = environment_list.objects.get(env = env , app_list__app = app, app_list__opco = opco)
        archives = build_archive.objects.filter(exec_count__env_opco_app__id = eao.id)
        builds = build_detail.objects.filter(id__in = archives.values('build_detail__id'))

        request.session = {
            'builds' : builds,
            'e_o_m' : self.env_opco_map,
            'd_n' : DASHBOARD_NAME,
            's_d_a_r' : SIDEBAR_DROPDOWN_AUTOMATION_REPORT,
            's_d_e_s' : SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS,
            'b_a_p_i' : BUILDS_ARCHIVE_PAGE_APP_INFO,
            'r_n' : RUNNING_IN,
            'page_title' : BUILDS_LIST_PAGE_TITLE,
            'env' : ENV,
            'app' : APP,
            'opco' : OPCO,
            'stat' : STATUS,
            'ts' : TIMESTAMP,
            'no' : BUILD_NO,
            }
        template = loader.get_template('dashboard/list_of_builds.html')           
        return HttpResponse(template.render(request.session, request))