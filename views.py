#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djing.settings")

import codecs
import urlparse
import urllib
from datetime import datetime
from django import template
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import smart_unicode
from djing.natal_render import NatalSvg
from djing.models import ChartInfo
from djing.models import getChartSets
from djing.utils import UserDefTZ



def testshow():
    cid = 1
    ci = ChartInfo.objects.get(id=1)
    natal = NatalSvg()
    cs = getChartSets(None)
    natal.load_conf(cs)
    natal.load_data(ci)
    
    svg_xml = natal.render()
    (ptable_data, htable_data, rtable_data) = natal.calc_planet_table_data()
    firdaria_result = natal.firdaria()
    

    h = render_to_string("natal.html",{"current":"natal",
         "chart_svg":svg_xml,
         "ptable_data":ptable_data,
         "htable_data":htable_data,
         "rtable_data":rtable_data,
         "firdaria_result":firdaria_result,
         "cid": cid,
         "ci":ci})

    f = codecs.open('html/natal.html', 'w', 'utf-8')
    f.write(h)
    f.close()

    return "html/natal.html"

def add():
    
    h = render_to_string("add.html",{"current":"add"})

    f = codecs.open('html/add.html', 'w', 'utf-8')
    f.write(h)
    f.close()

    return "html/add.html"

def add_action(qs):
    """chartinfo insert into db"""
    
    qd = urlparse.parse_qs(qs.decode("iso-8859-1").encode("utf-8"))
    qname = qd["qname"][0]
    gender = qd["gender"][0]
    location = qd["location"][0]
    latitude = float(qd["latitude"][0])
    longitude = float(qd["longitude"][0])
    n_date = datetime.strptime(qd["n_date"][0], '%Y-%m-%d %H:%M')
    n_tz = int(qd["n_tz"][0])
    hsys = qd["hsys"][0]
    is_pub = qd["is_pub"][0]

    tz = UserDefTZ(n_tz)
    n_date_tz = datetime(n_date.year,n_date.month,n_date.day,
        n_date.hour, n_date.minute, n_date.second,
        n_date.microsecond, tz)

    #save ChartInfo
    ci = ChartInfo()
    ci.qname = qname
    ci.gender = gender
    ci.location = location
    ci.latitude = latitude
    ci.longitude = longitude
    ci.n_date = n_date_tz
    ci.n_tz = n_tz
    ci.hsys = hsys
    ci.is_pub = is_pub

    ci.save()
    

def list():
    mycharts = ChartInfo.objects.all()
    
    paginator = Paginator(mycharts, 10) # Show 25 contacts per page

    page = 1

    try:
        chartinfos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        chartinfos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        chartinfos = paginator.page(paginator.num_pages)


    h = render_to_string("list.html",{"current":"list",
                                    "chartinfos":chartinfos})

    f = codecs.open('html/list.html', 'w', 'utf-8')
    f.write(h)
    f.close()

    return "html/list.html"




if __name__ == '__main__':
    testshow()