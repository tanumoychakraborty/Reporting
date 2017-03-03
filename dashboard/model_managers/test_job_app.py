'''
Created on 1 Mar 2017

@author: tanumoy chakraborty
'''

from django.db import models

class test_job_app_manager(models.Manager):
    def create_test_job_app(self,test_job_name,test_job_url,app):
        test_job_app = self.create(test_job_name=test_job_name, test_job_url=test_job_url, app=app)
        return test_job_app