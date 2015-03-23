# -*- coding: utf-8 -*-
import math
from datetime import timedelta, tzinfo
from string import Template
import settings
from svg_symbol import svg_symbol_dict
snames = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
"scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

def dechourjoin(inH , inM , inS ):
    dh = float(inH)
    dm = float(inM)/60
    ds = float(inS)/3600
    output = dh + dm + ds
    return output

def cmp_bodies(b1, b2):
    if   b1["degree_asc"] >  b2["degree_asc"]:
        return -1
    elif b1["degree_asc"] == b2["degree_asc"]:
        return 0
    else:
        return 1

#decimal to degrees (a°b"c')
def dec2deg(dec , type="3"):
    dec=float(dec)
    a=int(dec)
    a_new=(dec-float(a)) * 60.0
    b_rounded = int(round(a_new))
    b=int(a_new)
    c=int(round((a_new-float(b))*60.0))
    if type=="3":
        out = '%(#1)02d&#176;%(#2)02d&#34;%(#3)02d&#39;' % {'#1':a,'#2':b, '#3':c}
    elif type=="2":
        out = '%(#1)02d&#176;%(#2)02d' % {'#1':a,'#2':b_rounded}
    elif type=="1":
        out = '%(#1)02d&#176;' % {'#1':a}
    return str(out)

#degree difference
def degree_diff(a , b):
    out=float()
    if a > b:
        out=a-b
    if a < b:
        out=b-a
    if out > 180.0:
        out=360.0-out
    return out

def circle_degree_mid(a, b):
    a1 = a % 360
    b1 = b % 360
    if abs(a1 - b1) > 180:
        c1 = ((a1+b1)/2)-180
    else:
        c1 = (a1+b1)/2
    
    return c1


def X1(a, r, cx): #返回X坐标
    x = math.radians(a)
    return cx + r*math.cos(x)

def Y1(a, r, cy): #返回Y坐标
    x = math.radians(a)
    return cy + r*math.sin(x)

def test_aspect(body1, body2, deg1, deg2, delta, t1, t2, type):
    if not body1 == body2:
        orb = (float(t1)+float(t2))/2
        has_phase = False
        if  (deg1 > (deg2       + delta - orb) and deg1 < (deg2       + delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2)
            
        if  (deg1 > (deg2       - delta - orb) and deg1 < (deg2       - delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2)
            
        if  (deg1 > (deg2 + 360 + delta - orb) and deg1 < (deg2 + 360 + delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2 - 360)
            
        if  (deg1 > (deg2 - 360 + delta - orb) and deg1 < (deg2 - 360 + delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2 + 360)
            
        if  (deg1 > (deg2 + 360 - delta - orb) and deg1 < (deg2 + 360 - delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2 - 360)
            
        if  (deg1 > (deg2 - 360 - delta - orb) and deg1 < (deg2 - 360 - delta + orb)):
            has_phase = True
            angle = abs(deg1 - deg2 + 360)
        
        if has_phase == True:
            return (body1, body2, deg1, deg2, type, angle)
        else:
            return None

def svg_symbol(symbol, scale=1.5):
        td = dict()
        td['symbol'] = symbol
        td['symbol_svg'] = svg_symbol_dict[symbol]
        
        if symbol in snames:
            td['scale'] = 1
        else:
            td['scale'] = scale

        f = open(settings.SVG_SYMBOL_PATH)
        template = Template(f.read()).substitute(td)
        f.close()
        return template

class ChartSetsNoModel(object):
    def __init__(self):
        self.natal_planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "mean node", "Asc", "Mc"]
    
        self.natal_tolerance = {"sun":15, "moon":12, "mercury":7, "venus":7, "mars":8,\
                                             "jupiter":9, "saturn":9, "mean node":5, "Asc":0, "Mc":0}
        
        self.natal_phase = {"conjunction":0, "sextile":60, "square":90, "trine":120, "opposition":180}
        
        self.transit_planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",\
                            "uranus", "neptune", "pluto", "mean node"]
        
        self.transit_tolerance = {"sun":3, "moon":3, "mercury":3, "venus":3, "mars":3, "jupiter":3, "saturn":3,\
                            "uranus":3, "neptune":3, "pluto":3, "mean node":3, "Asc":3, "Mc":3}
        
        self.transit_phase = {"conjunction":0, "semi-square":45, "sextile":60, "square":90,\
                                           "trine":120, "sesquiquadrate":135, "quincunx":150, "opposition":180}
        
        self.firdaria_night_order = '0'
        
class UserDefTZ(tzinfo):
    def __init__(self, offset):
        self.offset = offset
    
    def utcoffset(self, dt):
        return timedelta(hours=self.offset)
    
    def dst(self, dt):
        return timedelta(0)
    
    def tzname(self):
        return "UTC " + str(self.offset)
