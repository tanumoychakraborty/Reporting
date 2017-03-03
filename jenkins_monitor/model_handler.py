'''
Created on 25 Jan 2017

@author: tanumoy chakraborty
'''
from dashboard.models import count, environment_list, latest_build, exec_count, \
    build_detail, build_archive, test_case, test_run, fitnesse_report, \
    pipeline_opco
from jenkins_monitor.__main__ import logger
from jenkins_monitor.jenkins_lib import convert_jenkins_timestamp


def get_blank_count():
    return count.objects.create_count(0,0,0,0,0.0)

def get_env_app_opco(env, app):
    try:
        return environment_list.objects.get(env = env , app_list__app = app)
    except environment_list.DoesNotExist:
        logger.info("Error :::: Specified environment "+env+" and application "+app+" does not exist in the Data Base")
        return None

def get_latest_build_by_url(url):
    latest = latest_build.objects.filter(last_build__build_detail__build_url__contains=url)
    build = build_archive.objects.get(id__in = latest.values('last_build__id'))
    return build.build_detail.build_no

def create_count(total,total_pass,total_fail,total_ignore,duration):
    return count.objects.create_count(total,total_pass,total_fail,total_ignore,duration)

def create_exec_count(count, env_opco_app):
    return exec_count.objects.create_exec_count(count, env_opco_app)

def create_build_detail(build_url,build_no,timestamp,status):
    ts = convert_jenkins_timestamp(timestamp)
    return build_detail.objects.create_build_detail(build_url,build_no,ts,status)

def create_build_archive(build_detail,exec_count):
    return build_archive.objects.create_build_archive(build_detail,exec_count)

def update_latest_build(env,build_archive,is_success):
    try:
        last_build = latest_build.objects.get(env=env)
    except latest_build.DoesNotExist:
        if is_success:
            last_build = latest_build.objects.create_latest_build(env, build_archive, build_archive)
        else:
            last_build = latest_build.objects.create_latest_build(env, build_archive, None)    
        last_build.save()
        return True, env
    if is_success:
        if last_build.last_successful_build is None:  
            last_build.last_successful_build = build_archive
        elif last_build.last_successful_build.build_detail.build_no<build_archive.build_detail.build_no:
            last_build.last_successful_build = build_archive
    if last_build.last_build.build_detail.build_no<build_archive.build_detail.build_no:
        last_build.last_build = build_archive
    last_build.save()
    return True, env
    

def create_test_case(test_case_name,app):
    return test_case.objects.create_test_case(test_case_name, app)

def create_test_run(test_cases,detail,status,duration):
    return test_run.objects.create_test_run(test_cases,detail,status,duration)

def create_fitnesse_report(build_detail):
    return fitnesse_report.objects.create_fitnesse_report(build_detail)

def update_pipeline_env(url, env):
    pipeline = pipeline_opco.objects.get(pipeline_url = url)
    pipeline.current_env = env
    pipeline.save()