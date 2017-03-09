'''
Created on 9 Jan 2017

@author: tanumoy chakraborty
'''
# import KITSReporting
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITSReporting.settings')"{}.settings".format(module)
# import sys
# 
# 
# sys.path.append(KITSReporting.settings.BASE_DIR) 

import django
import logging
import os
import sys
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# # create a file handler
# handler = logging.FileHandler('hello.log')
# handler.setLevel(logging.INFO)
# 
# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# 
# # add the handlers to the logger
# logger.addHandler(handler)


if __name__ == '__main__':
    '''
    Setup Django Environment to import the models
    '''
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITSReporting.settings')
    django.setup()
    
    
      
#    from jenkins_monitor.pickling import add_job_app_to_list
#     add_job_app_to_list("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/BQ/job/Pipelines/job/develop_resource/job/TestATG_AFA-Flow/","casto_agent")
#     print "hi"
#     add_job_app_to_list("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/BQ/job/Pipelines/job/develop_resource/job/TestATG_AFA-Flow/","AFA")
#     print "hi"
#     add_job_app_to_list("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/job/TestATG_AFA-Flow/","casto_agent")
#     print "hi"
#    resp = get_job_info("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/job/TestATG_AFA-Flow/104/fitnesseReport/fitnesse-results-agent-block1.html.xml/DarwinAcceptanceTests.IntegrationWebForAgent.TestForCloud.CheckoutWithNewCard/Details/")
#    print resp
#     from jenkins_monitor.ReadJenkins import read_j
#     __j__ = read_j("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/job/TestATG_AFA-Flow/","CASTO_AGENT")
#     code = __j__.syncJob()
#     from dashboard.dynamo_prod_util.common import getSearchEngineDictionary
#     r = getSearchEngineDictionary("http://atg-devops05-aws-app01.aws.gha.kfplc.com:8080")
#     print r
#     from jenkins_monitor.jenkins_lib import get_resp
#     r = get_resp("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/")
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"page.html")
#     if not os.path.exists(path):
#         with open(path, "w+") as fp: 
#             pickle.dump(r, fp)
#     from jenkins_monitor.jenkins_pipeline_view import PipelineView
#     pv = PipelineView("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/")
#     pv.replicatePipelineView()
#     from dashboard.models import test_job_app
#     from jenkins_monitor.model_handler import update_pipeline_env
#     j = test_job_app.objects.all()
#     update_pipeline_env("http://jenkins-master.aws.gha.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/","DEVOPS07")
#     print "hi"
    from jenkins_monitor.jenkins_pipeline_view import PipelineView
    from dashboard.templatetags.dashboard_extras import render_pipeline_view
    __p_v__ = PipelineView("http://jenkins-ecomm-master.aws.ghanp.kfplc.com:8080/job/ATG/job/Build/job/Casto/job/Pipelines/job/develop_resource/")
    _first_job, stages = __p_v__.replicatePipelineView()
    
    x = render_pipeline_view({"stages":stages, "first_job":_first_job})
    print x