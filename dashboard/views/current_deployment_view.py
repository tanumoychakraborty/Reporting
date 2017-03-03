'''
Created on 1 Mar 2017

@author: tanumoy chakraborty
'''
from django.http.response import HttpResponse
from django.template import loader

from dashboard.models import pipeline_opco
from dashboard.static.dashboard.messages.home import DASHBOARD_NAME, \
    SIDEBAR_DROPDOWN_AUTOMATION_REPORT, SIDEBAR_DROPDOWN_ENVIRONMENT_STATUS, \
    HOME_PAGE_LATEST_BUILDS_BLOCK, ENV, APP, OPCO, STATUS, TIMESTAMP, BUILD_NO, \
    HOME_PAGE_TITLE
from dashboard.views.basic_template_view import DashboardTemplate
from jenkins_monitor.jenkins_pipeline_view import PipelineView


class CurrentDeployment(DashboardTemplate):

    def get(self, request, env):
        pipeline_views = []
        __p_o__ = pipeline_opco.objects.filter(current_env = env)
        for _ in __p_o__:
            __p_v__ = PipelineView(_.pipeline_url)
            _first_job, stages = __p_v__.replicatePipelineView()
            pipeline_views.append({"first_job":_first_job, "stages":stages})
        request.session = {
            'e_o_m' : self.env_opco_map,
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
            'pplns' : pipeline_views,
            }
        template = loader.get_template('dashboard/view_pipeline.html')           
        return HttpResponse(template.render(request.session, request))
        
