'''
Created on 15 Feb 2017

@author: tanumoy chakraborty
'''
'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''

from django.http.response import HttpResponse

from dashboard.common.common_util import createHTMLFromFitnesseDetail
from dashboard.models import test_run
from dashboard.views.basic_template_view import DashboardTemplate


class ScenarioDetails(DashboardTemplate):
    
    def get(self, request, testrun):
        report = test_run.objects.get(id = testrun)
        detail = createHTMLFromFitnesseDetail(report.detail)
         
        return HttpResponse(detail)