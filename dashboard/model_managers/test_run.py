'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models


class test_run_manager(models.Manager):
    def create_test_run(self,test_cases,detail,status,duration):
        automation_report = self.create(test_cases=test_cases, detail=detail, status=status, duration=duration)
        return automation_report