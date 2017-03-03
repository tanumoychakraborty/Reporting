'''
Created on 29 Dec 2016

@author: Tanumoy
'''
from django.views import View

from dashboard.models import environment_list, pipeline_opco


class DashboardTemplate(View):


    def __init__(self):
        self.env_opco_map = {}
        self.env_list_fr_saved_pipelines = []
        e_l = environment_list.objects.all()
        for e in e_l:
            if e.app_list.opco in self.env_opco_map:
                if e.app_list.app in self.env_opco_map[e.app_list.opco]:
                    self.env_opco_map[e.app_list.opco][e.app_list.app].append(e.env)
                else:
                    self.env_opco_map[e.app_list.opco][e.app_list.app] = [e.env]
            else:
                self.env_opco_map[e.app_list.opco] = {e.app_list.app:[e.env]}
        
        p_o = pipeline_opco.objects.all()
        for p in p_o:
            self.env_list_fr_saved_pipelines.append(p.current_env)