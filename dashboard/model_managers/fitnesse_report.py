'''
Created on 9 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models

class fitnesse_report_manager(models.Manager):
    def create_fitnesse_report(self,build_detail):
        fitnesse_report = self.create(build_detail=build_detail)
        return fitnesse_report    
