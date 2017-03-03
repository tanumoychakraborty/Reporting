from django.contrib import admin

from dashboard.models import application_list, environment_list, count, \
    build_detail, test_case, test_run, exec_count, latest_build, \
    build_archive, fitnesse_report, application_host, test_job_app, pipeline_opco


# Register your models here.
admin.site.register(application_list)
admin.site.register(environment_list)
admin.site.register(count)
admin.site.register(build_detail)
admin.site.register(test_case)
admin.site.register(test_run)
admin.site.register(exec_count)
admin.site.register(build_archive)
admin.site.register(latest_build)
admin.site.register(fitnesse_report)
admin.site.register(application_host)
admin.site.register(test_job_app)
admin.site.register(pipeline_opco)