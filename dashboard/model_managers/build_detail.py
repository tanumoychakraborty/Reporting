'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models


class build_detail_manager(models.Manager):
    def create_build_detail(self,build_url,build_no,timestamp,status):
        build_detail = self.create(build_url=build_url, build_no=build_no, timestamp=timestamp, status=status)
        return build_detail