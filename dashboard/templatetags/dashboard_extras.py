'''
Created on 14 Feb 2017

@author: tanumoy chakraborty
'''

from django import template
from django.utils.safestring import mark_safe
register = template.Library()
arrow = "<svg style=\"position:absolute;left:15px;top:5px\" width=\"162\" height=\"102\" pointer-events=\"none\" position=\"absolute\" version=\"1.1\" xmlns=\"http://www.w3.org/1999/xhtml\" class=\"_jsPlumb_connector relation\"><path d=\"M 13,11 L 69 11 \" pointer-events=\"all\" version=\"1.1\" xmlns=\"http://www.w3.org/1999/xhtml\" style=\"\" fill=\"none\" stroke=\"#000000\" stroke-width=\"2\"></path><path pointer-events=\"all\" version=\"1.1\" xmlns=\"http://www.w3.org/1999/xhtml\" d=\"M69,11 L49,21 L56.53999999999999,11 L49,1 L69,11\" class=\"\" stroke=\"rgba(0,0,0,0.5)\" fill=\"rgba(0,0,0,0.5)\"></path></svg>"


@register.filter(name='render_pipeline')
def render_pipeline_view(dict):
    _max_child = 0
    for key, value in dict['stages'].iteritems():
        _max_child = value['downstreamStages'].__len__() if _max_child < value['downstreamStages'].__len__() else _max_child
    _first_job = dict['first_job']
    html = [[None]] * _max_child
    html[0]=["<button class=\"btn btn-success btn-lg\">"+_first_job+"</button>"]
    html = create_downstream_job_views(dict['stages'], _first_job, html)
    _pipeline_html = ""
    _down_arrow_count = 0
    
    for row in html:
        _right_arrow_count = 0
        _pipeline_html += "<div>"
        for col in row:
            if col == None:
                _pipeline_html += "<button style=\"width:120px; height:50px; color:#FFFFFF; opacity:0;\">  </button>"
            elif _right_arrow_count != 0:
                if row[_right_arrow_count-1] != None:
                    _pipeline_html += "<span class=\"glyphicon glyphicon-arrow-right\"></span>" + col
                else:
                    _pipeline_html += col
            else:
                _pipeline_html += col
            _right_arrow_count +=1
        _pipeline_html += "</div>"    
    _down_arrow_count += 1
        
    
    return mark_safe(_pipeline_html)
        

def create_downstream_job_views(dict, current_job, html):
    downstream_count = dict[current_job]['downstreamStages'].__len__()
    if downstream_count != 0:
        _row = 0
        for h in html:
            h.append(None)
        __pos__ = html[_row].__len__() - 1
        for job in dict[current_job]['downstreamStages']:
            html[_row][__pos__] = "<button class=\"btn btn-success btn-lg\">"+job+"</button>"
            html = create_downstream_job_views(dict, job, html)
            _row+=1
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