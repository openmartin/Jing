# -*- coding: utf-8 -*-
import os
import sys
import math
from datetime import datetime
from utils import dechourjoin

import swisseph as swe
from settings import SWE_DATAFILE_PATH
swe.set_ephe_path(SWE_DATAFILE_PATH)

bnames = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",\
          "uranus", "neptune", "pluto", "mean node"]
#swisseph 中 星体代码
bnames_se = {"sun":0, "moon":1, "mercury":2, "venus":3, "mars":4, "jupiter":5, \
          "saturn":6, "uranus":7, "neptune":8, "pluto":9, "mean node":10}
anames = ["Asc", "Mc"]
#十二星座
snames = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
"scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

DEFAULT_DATE = datetime(1990, 3, 30, 18, 15, 0)

class swissephData:

    def __init__(self):
        self.cibodies  = []
        self.cihouses  = []
        self.ciascmcs  = []
        self.ciresults = {}
    
    def calc(self, lat=0.0, lon=0.0, i_date=DEFAULT_DATE, hsys='P'):
        year = i_date.year
        month = i_date.month
        day = i_date.day
        time = dechourjoin(i_date.hour, i_date.minute, i_date.second)
        
        julday = swe.julday(year, month, day, time)
        geo = swe.set_topo(lat, lon, 0)
        houses, ascmc = swe.houses(julday, lat, lon,  hsys)
        #print houses
        
        for i, body in enumerate(bnames): #日月水金火木土天海冥北交
            result = swe.calc_ut(julday, bnames_se[body])
            degree_ut = result[0]; #和春分点的夹角
            retrograde = bool(result[3] < 0) #是否逆行
            
            for sign in range(12): #行星在12星座的什么位置
                deg_low =  float(sign * 30)
                deg_high = float((sign + 1) * 30)
                if (degree_ut >= deg_low and degree_ut <= deg_high):
                    cibody = { "id"         : bnames_se[body],
                               "name"       : body,
                               "sign"       : sign,
                               "sign_name"  : snames[sign],
                               "degree"     : degree_ut - deg_low, #相对星座头部的夹角
                               "degree_ut"  : degree_ut, #和春分点的夹角
                               "retrograde" : retrograde } #是否逆行
                    self.cibodies.append(cibody)
                    
        for index, degree_ut in enumerate(houses): #十二宫的位置
            for sign in range(12):
                deg_low =  float(sign * 30)
                deg_high = float((sign + 1) * 30)
                if (degree_ut >= deg_low and degree_ut <= deg_high):
                    cihouse = { "id"         : index + 1,
                                "name"       : "House",
                                "sign"       : sign,
                                "sign_name"  : snames[sign],
                                "degree"     : degree_ut - deg_low,
                                "degree_ut"  : degree_ut }
                    self.cihouses.append(cihouse)
                    
        for index in range(2): #上升点和天顶
            degree_ut = ascmc[index]
            for sign in range(12):
                deg_low =  float(sign * 30)
                deg_high = float((sign + 1) * 30)
                if (degree_ut >= deg_low and degree_ut <= deg_high):
                    ciascmc = { "id"         : index + 1,
                                "name"       : anames[index],
                                "sign"       : sign,
                                "sign_name"  : snames[sign],
                                "degree"     : degree_ut - deg_low,
                                "degree_ut"  : degree_ut }
                    self.ciascmcs.append(ciascmc)
                    cibody  = { "id"         : anames[index],
                                "name"       : anames[index],
                                "sign"       : sign,
                                "sign_name"  : snames[sign],
                                "degree"     : degree_ut - deg_low,
                                "degree_ut"  : degree_ut,
                                "retrograde" : None }
                    self.cibodies.append(cibody)
        
        swe.close()
        
        ciresults = {
            "bodies"  : self.cibodies,
            "houses"  : self.cihouses,
            "ascmcs"  : self.ciascmcs
            }
    
        return ciresults

def to_xml(results):
    xml_str = "<?xml version='1.0' encoding='UTF-8'?>\n"
    chart_str = "<chartinfo>\n"
    xml_str += chart_str
    for partk,partv in results.iteritems():
        part_str = "  <"+partk+">\n"
        for item in partv:
            row_str = "    <"+str(item["name"])+" "
            for argk,argv in item.iteritems():
                if argk != "name":
                    row_str = row_str + argk + "=\"" + str(argv) + "\" "
            row_str += "/>\n"
            part_str += row_str
        part_str += "  </"+partk+">\n"
        xml_str += part_str
    xml_str += "</chartinfo>\n"
    return xml_str

if __name__ == '__main__':
    swissCalc = swissephData()
    now_date = datetime.now()
    results = swissCalc.calc(113.30579,30.37518, now_date, 'P')
    print results
    xml_str = to_xml(results)
    print xml_str
