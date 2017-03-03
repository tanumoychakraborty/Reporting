'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models

class count_manager(models.Manager):
    def create_count(self,total,right,wrong,ignore,duration):
        exec_count = self.create(total=total, right=right, wrong=wrong, ignore=ignore, duration=duration)
        return exec_count