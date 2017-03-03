'''
Created on 23 Jan 2017

@author: tanumoy chakraborty
'''
import os
import pickle


# def add_job_app_to_list(url, app):
#     new = True
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"job_app_list")
#     if not os.path.exists(path):
#         with open(path, "w+") as fp: 
#             pickle.dump([{"url":url,"app":app}], fp)
#             return
#     with open (path, 'rb') as fp:
#         job_app_list = pickle.load(fp)
#     for job_app in job_app_list:
#         if job_app['url'] == url:
#             job_app['app'] = app
#             new = False
#             break
#     if new:
#         job_app_list.append({"url":url,"app":app})
#     with open(path, "wb") as fp: 
#         pickle.dump(job_app_list, fp)
#         
# def get_job_app_list():
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"job_app_list")
#     with open (path, 'rb') as fp:
#         job_app_list = pickle.load(fp)
#     return job_app_list

def save_daemon_process_id(process_info):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"j_daemon")
    with open (path, 'wb') as fp:
            pickle.dump(process_info,fp)
