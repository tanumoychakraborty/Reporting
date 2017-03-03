from __future__ import unicode_literals

from django.db import models

from dashboard.model_managers.application_hosts import application_host_manager
from dashboard.model_managers.application_list import application_list_manager
from dashboard.model_managers.build_archive import build_archive_manager
from dashboard.model_managers.build_detail import build_detail_manager
from dashboard.model_managers.count import count_manager
from dashboard.model_managers.environment_list import environment_list_manager
from dashboard.model_managers.exec_count import exec_count_manager
from dashboard.model_managers.fitnesse_report import fitnesse_report_manager
from dashboard.model_managers.latest_build import latest_build_manager
from dashboard.model_managers.pipeline_opco import pipeline_opco_manager
from dashboard.model_managers.test_case import test_case_manager
from dashboard.model_managers.test_job_app import test_job_app_manager
from dashboard.model_managers.test_run import test_run_manager


class test_job_app(models.Model):
    test_job_name = models.CharField(max_length=50, null=False)
    test_job_url = models.CharField(max_length=1000, null=False)
    app = models.CharField(max_length=15, null=False)
    objects = test_job_app_manager()
    def __str__(self):
        return self.test_job_name + ' & ' + self.app


class pipeline_opco(models.Model):
    pipeline_name = models.CharField(max_length=50, null=False)
    pipeline_url = models.CharField(max_length=1000, null=False)
    opco = models.CharField(max_length=15, null=False)
    current_env = models.CharField(max_length=15, default=None)
    test_job_app = models.ManyToManyField(test_job_app)
    objects = pipeline_opco_manager()
    def __str__(self):
        return self.pipeline_name + ' & ' + self.opco
    
    
class application_list(models.Model):
    opco = models.CharField(max_length=15)
    app = models.CharField(max_length=20)
    objects = application_list_manager()
    
    def __str__(self):
        return self.opco + ' & ' + self.app
    

class environment_list(models.Model):
    app_list = models.ForeignKey(application_list)
    env = models.CharField(max_length=20)
    objects = environment_list_manager()
    
    def __str__(self):
        return self.env + ' & ' + self.app_list.opco + ' & ' + self.app_list.app
    
class count(models.Model):
    total = models.IntegerField(default=0)
    right = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    ignore = models.IntegerField(default=0)
    duration = models.FloatField(default=0.0)
    objects = count_manager()
        
    def __str__(self):
        return 'T ' + str(self.total) + ' R ' + str(self.right) + ' W ' + str(self.wrong) + ' I ' + str(self.ignore)
    
class build_detail(models.Model):
    build_url = models.CharField(max_length=1000)
    build_no = models.IntegerField(default=-1)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=20,default='default')
    objects = build_detail_manager()
    
    def __str__(self):
        return self.build_url + ' & ' + str(self.build_no) + ' & ' + self.status    

class test_case(models.Model):
    test_case_name = models.CharField(max_length = 100)
    app = models.ForeignKey(application_list)
    objects = test_case_manager()
    
    def __str__(self):
        return self.app.opco + ' & ' + self.test_case_name
    
class test_run(models.Model):
    test_cases = models.ForeignKey(test_case)
    detail = models.CharField(max_length = 5000000,default='No Execution Detail')
    status = models.CharField(max_length = 15)
    duration = models.FloatField(default=0.0)
    objects = test_run_manager()
    
    def __str__(self):
        return self.test_cases.test_case_name + ' & ' + self.status

class exec_count(models.Model):
    count = models.ForeignKey(count)
    env_opco_app = models.ForeignKey(environment_list,default=None)
    objects = exec_count_manager()
    
    def __str__(self):
        return str(self.count.total) + ' & ' + str(self.env_opco_app)
    
class build_archive(models.Model):
    build_detail = models.ForeignKey(build_detail)
    exec_count = models.ForeignKey(exec_count)
    objects = build_archive_manager()
    
    def __str__(self):
        return self.build_detail.build_url + ' & ' + str(self.exec_count.count.total)

class latest_build(models.Model):
    env = models.CharField(max_length = 15)
    last_build = models.ForeignKey(build_archive,related_name='last_build')
    last_successful_build = models.ForeignKey(build_archive,null=True,related_name='last_successful_build')
    objects = latest_build_manager()
    
    def __str__(self):
        return str(self.last_build)#self.env + ' & ' + self.last_build.build_detail.build_url
    
class fitnesse_report(models.Model):
    build_detail = models.ForeignKey(build_detail)
    test_run = models.ManyToManyField(test_run)
    objects = fitnesse_report_manager()
    
    def __str__(self):
        return str(self.build_detail) + str(self.test_run)
    
class application_host(models.Model):
    host = models.CharField(max_length = 100)
    env_opco_app = models.ForeignKey(environment_list)
    objects = application_host_manager()
    
    def __str__(self):
        return str(self.host) + ' & ' + str(self.env_opco_app)