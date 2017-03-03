'''
Created on 1 Mar 2017

@author: tanumoy chakraborty
'''

from django.db import models

class pipeline_opco_manager(models.Manager):
    def create_pipeline_opco(self,pipeline_name,pipeline_url,opco,current_env):
        pipeline_opco = self.create(pipeline_name=pipeline_name, pipeline_url=pipeline_url, opco=opco, current_env=current_env)
        return pipeline_opco