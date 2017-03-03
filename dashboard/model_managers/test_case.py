'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models


class test_case_manager(models.Manager):
    def create_test_case(self,test_case_name,app):
        test_case = self.create(test_case_name=test_case_name, app=app)
        return test_case