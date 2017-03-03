'''
Created on 12 Jan 2017

@author: tanumoy chakraborty
'''
import django
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# # create a file handler
handler = logging.FileHandler('dashboard.log')
handler.setLevel(logging.INFO)
# 
# # create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# 
# # add the handlers to the logger
logger.addHandler(handler)

if __name__ == '__main__':
    '''
    Setup Django Environment to import the models
    '''
    logger.info("Importing Environment from Django")
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITSReporting.settings')
    django.setup()
    
    '''
    READ
    '''
    from jenkins_monitor.start import start
    start()