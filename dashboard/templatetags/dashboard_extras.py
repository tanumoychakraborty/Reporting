'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''

from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter(name='render_pipeline')
def render_pipeline_view(dict):
    _first_job = dict['first_job']
    slic = 12
    html = "<p class=\"center-block\"><span class=\"btn btn-success btn-lg\">"+_first_job+"</span></p>"
    html = create_downstream_job_views(dict['stages'], _first_job, html, slic)
    print html
    return mark_safe(html)
        

def create_downstream_job_views(dict, current_job, html, slic):
    downstream_count = dict[current_job]['downstreamStages'].__len__()
    if downstream_count != 0:
        slic /= downstream_count
        html += "<div class=\"row\">"
        for job in dict[current_job]['downstreamStages']:
            html = html + "<div class=\"col-xs-"+str(slic)+" text-center\">"+\
                    "<p class=\"btn\"><span class=\"glyphicon glyphicon-arrow-down\"></span>"+\
                    "<p class=\"center-block\"><span class=\"btn btn-success btn-lg\">"+job+"</span></p>"+\
                    "</div>"
            html = create_downstream_job_views(dict, job, html, slic)
        html += "</div>"
    return html



@register.filter(name='prc')
def compute_percentage(value, total):
    if value == 0 or total == 0:
        return 0.0
    dmt = get_in_hundreds(total)
    perc = dmt*float(value)/float(total)
    return perc

def get_in_hundreds(v):
    r = 10
    while True:
        if int(v)/r > 0:
            r = r*10
        else:
            break
    return r