'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from requests.exceptions import HTTPError

from jenkins_monitor.__main__ import logger
from jenkins_monitor.jenkins_lib import get_job_info, get_environment, \
    getFitnesseReportUrl, getApiUrl, get_fitnesse_page_detail, \
    formatFitnesseTestDesc
from jenkins_monitor.model_handler import get_env_app_opco, \
    create_build_detail, create_build_archive, create_exec_count, create_count, \
    update_latest_build, get_blank_count, create_test_case, create_test_run, \
    create_fitnesse_report, update_pipeline_env


class jHelperClass(object):
    '''
    classdocs
    '''
    
    def __init__(self, app, buildsNotSaved, pipeline_url):
        self.app = app
        self.buildsNotSaved = buildsNotSaved
        self.pipeline_url = pipeline_url
        self.blocks = []
        self.env_opco_app = None
        self.build_detail = None
        self.env_in_latest_build = ""
        
    
    def saveNewBuilds(self):
        urls = map(lambda x: x['url'], self.buildsNotSaved)
        saved = map(self.saveNewBuild, urls)
        update_pipeline_env(self.pipeline_url, self.env_in_latest_build)
        return saved
        
        
    def saveNewBuild(self, url):
        try:
            detail = get_job_info(url)
            env = get_environment(detail).upper()
            duration = detail['duration']
            timestamp = detail['timestamp']
            status = detail['result']
            build_no = detail['number']
            is_building = detail['building']
            is_success = not is_building
            automation_report_ok = False
            self.blocks = []
            if not is_building:
                count = self.getCount(duration, url)
                self.env_opco_app = get_env_app_opco(env, self.app)
                if self.env_opco_app is None:
                    pass 
                exec_count = create_exec_count(count, self.env_opco_app)
                self.build_detail = create_build_detail(url, build_no, timestamp, status)
                build_archive = create_build_archive(self.build_detail, exec_count)
                
                is_success = True if not is_building and (status=='SUCCESS' or status =='UNSTABLE') else False
                
                if is_success:
                    try:
                        test_run = self.getTestRuns(url)
                        automation_report_ok = True
                        
                    except KeyError as e:
                        logger.info("Error. Jenkins doesn't like this automation report..... {0} ..... {1}".format(e, url))
                        build_archive.exec_count.count=get_blank_count()
                        
                build_archive.save()
                build, self.env_in_latest_build = update_latest_build(env,build_archive,is_success)
                if build:
                    logger.info("Latest build got updated with "+url)
                else:
                    logger.info("Latest build was not updated for "+url)
                if automation_report_ok:
                    map(lambda x: x.save(), test_run)
                    f_report = create_fitnesse_report(self.build_detail)
                    f_report.save()
                    map(lambda x: f_report.test_run.add(x), test_run)
                    
            return True
                        
        except KeyError as e:
            logger.info("Error. Jenkins doesn't like this build..... {0} ..... {1}".format(e, url))
            return True

        
    def getCount(self, duration, url):
        url = getApiUrl(getFitnesseReportUrl(url))  
        try:
            detail = get_job_info(url)
            children = detail['children']
            total_pass = total_fail = total_ignore = 0
            for child in children:
                total_pass += int(child['passCount'])
                total_fail += int(child['failCount'])
                total_ignore += int(child['ignoredCount'])
                self.blocks.append(child['name'])
            total = total_pass + total_fail + total_ignore
            count = create_count(total, total_pass, total_fail, total_ignore, duration)
            logger.info("scenario count "+str(count.total)+" for " + url)
        except HTTPError:
            logger.info("no result for this build " + url)   
            return get_blank_count() 
        return count
    
    
    def getTestRuns(self, url):
        test_run = []
        testRuns = map(lambda x: self.addTestRunsToList(getFitnesseReportUrl(url)+x+"/"), self.blocks)
        for testRun in testRuns:
            test_run.extend(testRun)
        return test_run


    def addTestRunsToList(self, url):
        detail = get_job_info(getApiUrl(url))
        failed = detail['failedTests'] if int(detail['failCount']) > 0 else None
        passed = detail['passedTests'] if int(detail['passCount']) > 0 else None
        ignored = detail['ignoredTests'] if int(detail['ignoredCount']) > 0 else None
        testRun = []
        if failed is not None:
            testRun.extend(map(lambda x: create_test_run(create_test_case(x['name'], self.env_opco_app.app_list), self.getFitnesseTestRunDetails(url, x['name']), 'FAIL', x['duration']), failed))
        if passed is not None:
            testRun.extend(map(lambda x: create_test_run(create_test_case(x['name'], self.env_opco_app.app_list), self.getFitnesseTestRunDetails(url, x['name']), 'PASS', x['duration']), passed))
        if ignored is not None:
            testRun.extend(map(lambda x: create_test_run(create_test_case(x['name'], self.env_opco_app.app_list), self.getFitnesseTestRunDetails(url, x['name']), 'IGNORE', x['duration']), ignored))
        return testRun
            
                                    
            
    def getFitnesseTestRunDetails(self, url, name):
        detail = get_fitnesse_page_detail(url+name)
        return formatFitnesseTestDesc(detail)