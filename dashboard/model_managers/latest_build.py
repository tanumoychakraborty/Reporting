'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models



class latest_build_manager(models.Manager):
    
    def create_latest_build(self,environment,build_archive,successful_build_archive):
        last_build = self.create(env=environment, last_build=build_archive, last_successful_build=successful_build_archive)
        return last_build
    
    
    def get_last_five_builds(self):
        from dashboard.models import latest_build
        try:
            ids = latest_build.objects.values_list('last_build', flat=True).order_by('-id')[:5]
            
        except latest_build.DoesNotExist:
            print "latest build table is empty"
            return None
        from dashboard.models import build_archive
        return build_archive.objects.filter(pk__in = set(ids))

                    
        
            