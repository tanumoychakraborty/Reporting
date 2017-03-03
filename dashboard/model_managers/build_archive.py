'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models

class build_archive_manager(models.Manager):
    def create_build_archive(self,build_detail,exec_count):
        build_archive = self.create(build_detail=build_detail, exec_count=exec_count)
        return build_archive