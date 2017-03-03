'''
Created on 28 Dec 2016

@author: tanumoy chakraborty
'''
from django.conf.urls import url

from dashboard.views.automation_report_view import AutomationReport
from dashboard.views.build_detail_view import BuildDetail
from dashboard.views.builds_archive_view import BuildsArchive
from dashboard.views.compare_scenario_view import CompareScenario
from dashboard.views.current_deployment_view import CurrentDeployment
from dashboard.views.home_view import HomeView
from dashboard.views.scenario_details_view import ScenarioDetails
from dashboard.views.search_engines_view import SearchEngines


urlpatterns = [url(r'^$', HomeView.as_view(), name='index'),
               url(r'^build-detail/(?P<build>[0-9]+)$', BuildDetail.as_view(), name='build'),
               url(r'^automation-report/(?P<build>[0-9]+)$', AutomationReport.as_view(), name='automation_report'),
               url(r'^builds/(?P<opco>[a-zA-Z0-9_&]+)/(?P<app>[a-zA-Z0-9_&]+)/(?P<env>[a-zA-Z0-9_&]+)/$', BuildsArchive.as_view(), name='builds'),
               url(r'^automationreportdetail/(?P<testrun>[0-9]+)/$', ScenarioDetails.as_view(), name='automation_report_detail'),
               url(r'^comparescenarios/$', CompareScenario.as_view(), name='compare_scenario'),
               url(r'^search-engines/(?P<opco>[a-zA-Z0-9_&]+)/(?P<app>[a-zA-Z0-9_&]+)/(?P<env>[a-zA-Z0-9_&]+)/$', SearchEngines.as_view(), name='search_engines'),
               url(r'^current-deployments/(?P<env>[a-zA-Z0-9_&]+)/$', CurrentDeployment.as_view(), name='current-deployments'),
               ]