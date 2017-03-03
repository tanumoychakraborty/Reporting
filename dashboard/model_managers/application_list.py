'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''

from django.db import models

class application_list_manager(models.Manager):
    def create_application_list(self,opco,app):
        application_list = self.create(opco=opco, app=app)
        return application_list