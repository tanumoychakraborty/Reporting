'''
Created on 15 Feb 2017

@author: tanumoy chakraborty
'''
from django.core.exceptions import MultipleObjectsReturned

from dashboard.models import fitnesse_report, test_run, build_archive


def createScenarioCompareIntermediateList(i):
    i_d = {}
    __i_l__ = []
    t_r = test_run.objects.get(id=i)
    name = t_r.test_cases.test_case_name
    i_d['name'] = name
    aoe = getEnvOpcoAppFromTestRun(i)
    bs = build_archive.objects.filter(exec_count__env_opco_app__id=aoe.id).values_list('build_detail', flat=True).order_by('id')[:20]
    f_r = fitnesse_report.objects.filter(build_detail__id__in = bs)
    for r in f_r:
        d = {}
        #f = fitnesse_report.objects.get(id = r.id)
        d['build_no'] = r.build_detail.build_no
        try:
            tr = r.test_run.get(test_cases__test_case_name__exact = name)
            d['status'] = tr.status
            d['id'] = tr.id 
        except (fitnesse_report.DoesNotExist, test_run.DoesNotExist):
            d['status'] = "No Run"
            d['id'] = ""            
        
        except MultipleObjectsReturned:
            '''
            handle suite setup and suite teardown
            r.test_run.filter(test_cases__test_case_name__exact = name)
            '''
            return
        __i_l__.append(d)
    i_d['history'] = __i_l__    
    return i_d
   
def getEnvOpcoAppFromTestRun(testrun):
    f_r = fitnesse_report.objects.get(test_run=testrun)
    b_a = build_archive.objects.get(build_detail=f_r.build_detail)
    aoe = b_a.exec_count.env_opco_app
    return aoe

def getEnvOpcoAppFromBuild(build):
    f_r = fitnesse_report.objects.get(build_detail=build)
    b_a = build_archive.objects.get(build_detail=f_r.build_detail)
    aoe = b_a.exec_count.env_opco_app
    return aoe
        