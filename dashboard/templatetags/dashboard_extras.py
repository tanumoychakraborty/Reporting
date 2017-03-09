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
    html = [[None]]# * ((_max_child * 2) - 1)
    
    html[0]=["<td align=\"center\">"+getButtonFromColor(dict['stages'][_first_job]['color'], _first_job)+"</td>"]
    html = create_downstream_job_views(dict['stages'], _first_job, html)
    
    _pipeline_html = ""
    
    max_column = max(map(lambda x: x.__len__(), html))
    for tr in html:
        _pipeline_html += "<tr>"
        if tr.__len__() < max_column:
            tr.extend(map(lambda x: "<td align=\"center\"></td>", range(tr.__len__(), max_column)))
    
        _pipeline_html += reduce(lambda x,y: x+y, tr)
        _pipeline_html += "</tr>"
    
    return mark_safe(_pipeline_html)
        

def create_downstream_job_views(dict, current_job, html):
    downstream_count = dict[current_job]['downstreamStages'].__len__()
    if downstream_count != 0:
        _child_no = 0
        __pos__ = [html.__len__()-1, html[_child_no].__len__()-1]
        for job in dict[current_job]['downstreamStages']:
            if _child_no == 0:
                html[__pos__[0]].append("<td align=\"center\"><span class=\"glyphicon glyphicon-arrow-right\" style=\"padding-top:120%;\"></span></td>")
                html[__pos__[0]].append("<td align=\"center\">"+getButtonFromColor(dict[job]['color'], job)+"</td>")
            
            else:
                html.append(["<td align=\"center\"></td>"]*__pos__[1])
                html.append(["<td align=\"center\"></td>"]*__pos__[1])
                for i in range(__pos__[0]+1, html.__len__()):
                    if html[i].__len__() == 0:
                        html[i] = ["<td align=\"center\"><span class=\"glyphicon glyphicon-arrow-down\"></span></td>"]
                        html[i+1] = ["<td align=\"center\">"+getButtonFromColor(dict[job]['color'], job)+"</td>"]
                        break
                    elif all(x == "<td align=\"center\"></td>" for x in html[i]):
                        html[i][__pos__[1]] = "<td align=\"center\"><span class=\"glyphicon glyphicon-arrow-down\"></span></td>"
                        html[i+1][__pos__[1]] = "<td align=\"center\">"+getButtonFromColor(dict[job]['color'], job)+"</td>"
                        break
            html = create_downstream_job_views(dict, job, html)    
            _child_no+=2
    return html


def getButtonFromColor(color,job):
    if color == "blue":
        return "<button class=\"btn btn-success btn-lg\">"+job+"</button></td>"
    
    if color == "yellow":
        return "<button class=\"btn btn-warning btn-lg\">"+job+"</button></td>"
    
    if color == "red":
        return "<button class=\"btn btn-danger btn-lg\">"+job+"</button></td>"
    
    if "anim" in color:
        return "<button class=\"btn btn-info btn-lg\">"+job+"</button></td>"

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