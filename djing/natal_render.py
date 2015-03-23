# -*- coding: utf-8 -*-
from swe_data import swissephData, bnames, anames, snames
from string import Template
import math
import pytz
import codecs
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from djing.models import ChartInfo
from utils import cmp_bodies, dec2deg, dechourjoin, degree_diff, X1, Y1, test_aspect, svg_symbol, UserDefTZ, circle_degree_mid
from svg_symbol import svg_symbol_dict
from settings import NATAL_TEMPLATE_PATH

aspect_rel_color = {"conjunction":"#5757e2", "sextile":"#d59e28", "square":"#dc0000", "trine":"#36d100", "opposition":"#510060"}
aspect_rel_symbol = {"conjunction":"orb0", "sextile":"orb60", "square":"orb90", "trine":"orb120", "opposition":"orb180"}
#sname_small = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", 
#"scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
bnames_small = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"] #古典占星论法，没有三王星，Asc，Mc
bnames_small_rev = deepcopy(bnames_small)
bnames_small_rev.reverse()

ruler_of_zodiac = \
[
{"name":"aries", "id":1 , "ruler":"mars", "exalt":"sun", "fall":"saturn", "detr":"venus"},
{"name":"taurus", "id":2 , "ruler":"venus", "exalt":"moon", "fall":None, "detr":"mars"},
{"name":"gemini", "id":3 , "ruler":"mercury", "exalt":None, "fall":None, "detr":"jupiter"},
{"name":"cancer", "id":4 , "ruler":"moon", "exalt":"jupiter", "fall":"mars", "detr":"saturn"},
{"name":"leo", "id":5 , "ruler":"sun", "exalt":None, "fall":None, "detr":"saturn"},
{"name":"virgo", "id":6 , "ruler":"mercury", "exalt":None, "fall":"venus", "detr":"jupiter"},
{"name":"libra", "id":7 , "ruler":"venus", "exalt":"saturn", "fall":"sun", "detr":"mars"},
{"name":"scorpio", "id":8 , "ruler":"mars", "exalt":None, "fall":"moon", "detr":"venus"},
{"name":"sagittarius", "id":9 , "ruler":"jupiter", "exalt":None, "fall":None, "detr":"mercury"},
{"name":"capricorn", "id":10 , "ruler":"saturn", "exalt":"mars", "fall":"jupiter", "detr":"moon"},
{"name":"aquarius", "id":11 , "ruler":"saturn", "exalt":None, "fall":None, "detr":"sun"},
{"name":"pisces", "id":12 , "ruler":"jupiter", "exalt":"venus", "fall":None, "detr":"mercury"}
]

triple_of_zodiac = \
[
{"name":"aries", "id":1 ,       "triple":["sun", "jupiter", "saturn"]},
{"name":"taurus", "id":2 ,      "triple":["venus", "moon", "mars"]},
{"name":"gemini", "id":3 ,      "triple":["saturn", "mercury", "jupiter"]},
{"name":"cancer", "id":4 ,      "triple":["venus", "mars", "moon"]},
{"name":"leo", "id":5 ,         "triple":["sun", "jupiter", "saturn"]},
{"name":"virgo", "id":6 ,       "triple":["venus", "moon", "mars"]},
{"name":"libra", "id":7 ,       "triple":["saturn", "mercury", "jupiter"]},
{"name":"scorpio", "id":8 ,     "triple":["venus", "mars", "moon"]},
{"name":"sagittarius", "id":9 , "triple":["sun", "jupiter", "saturn"]},
{"name":"capricorn", "id":10 ,  "triple":["venus", "moon", "mars"]},
{"name":"aquarius", "id":11 ,   "triple":["saturn", "mercury", "jupiter"]},
{"name":"pisces", "id":12 ,     "triple":["venus", "mars", "moon"]}
]

term_of_zodiac = \
[
{"name":"aries", "id":1 ,       "term":[(0,6, "jupiter"),(6,12, "venus"),(12,20, "mercury"),(20,25, "mars"),(25,30, "saturn")]},
{"name":"taurus", "id":2 ,      "term":[(0,8, "venus"),(8,14, "mercury"),(14,22, "jupiter"),(22,27, "saturn"),(27,30, "mars")]},
{"name":"gemini", "id":3 ,      "term":[(0,6, "mercury"),(6,12, "jupiter"),(12,17, "venus"),(17,24, "mars"),(24,30, "saturn")]},
{"name":"cancer", "id":4 ,      "term":[(0,7, "mars"),(7,13, "venus"),(13,19, "mercury"),(19,26, "jupiter"),(26,30, "saturn")]},
{"name":"leo", "id":5 ,         "term":[(0,6, "jupiter"),(6,11, "venus"),(11,18, "saturn"),(18,24, "mercury"),(24,30, "mars")]},
{"name":"virgo", "id":6 ,       "term":[(0,7, "mercury"),(7,17, "venus"),(17,21, "jupiter"),(21,28, "mars"),(28,30, "saturn")]},
{"name":"libra", "id":7 ,       "term":[(0,6, "saturn"),(6,14, "mercury"),(14,21, "jupiter"),(21,28, "venus"),(28,30, "mars")]},
{"name":"scorpio", "id":8 ,     "term":[(0,7, "mars"),(7,11, "venus"),(11,19, "mercury"),(19,24, "jupiter"),(24,30, "saturn")]},
{"name":"sagittarius", "id":9 , "term":[(0,12, "jupiter"),(12,17, "venus"),(17,21, "mercury"),(21,26, "saturn"),(26,30, "mars")]},
{"name":"capricorn", "id":10 ,  "term":[(0,7, "mercury"),(7,14, "jupiter"),(14,22, "venus"),(22,26, "saturn"),(26,30, "mars")]},
{"name":"aquarius", "id":11 ,   "term":[(0,7, "mercury"),(7,13, "venus"),(13,20, "jupiter"),(20,25, "mars"),(25,30, "saturn")]},
{"name":"pisces", "id":12 ,     "term":[(0,12, "venus"),(12,16, "jupiter"),(16,19, "mercury"),(19,28, "mars"),(28,30, "saturn")]}
]

face_of_zodiac = \
[
{"name":"aries", "id":1 ,       "face":[(0,10, "mars"),(10,20, "sun"),(20,30, "venus")]},
{"name":"taurus", "id":2 ,      "face":[(0,10, "mercury"),(10,20, "moon"),(20,30, "saturn")]},
{"name":"gemini", "id":3 ,      "face":[(0,10, "jupiter"),(10,20, "mars"),(20,30, "sun")]},
{"name":"cancer", "id":4 ,      "face":[(0,10, "venus"),(10,20, "mercury"),(20,30, "moon")]},
{"name":"leo", "id":5 ,         "face":[(0,10, "saturn"),(10,20, "jupiter"),(20,30, "mars")]},
{"name":"virgo", "id":6 ,       "face":[(0,10, "sun"),(10,20, "venus"),(20,30, "mercury")]},
{"name":"libra", "id":7 ,       "face":[(0,10, "moon"),(10,20, "saturn"),(20,30, "jupiter")]},
{"name":"scorpio", "id":8 ,     "face":[(0,10, "mars"),(10,20, "sun"),(20,30, "venus")]},
{"name":"sagittarius", "id":9 , "face":[(0,10, "mercury"),(10,20, "moon"),(20,30, "saturn")]},
{"name":"capricorn", "id":10 ,  "face":[(0,10, "jupiter"),(10,20, "mars"),(20,30, "sun")]},
{"name":"aquarius", "id":11 ,   "face":[(0,10, "venus"),(10,20, "mercury"),(20,30, "moon")]},
{"name":"pisces", "id":12 ,     "face":[(0,10, "saturn"),(10,20, "jupiter"),(20,30, "mars")]}
]


class NatalSvg():
    
    def __init__(self):
        self.result = dict()
        
    def load_conf(self, cs):
        self.conf_natal_planets = cs.natal_planets
        self.conf_natal_tolerance = cs.natal_tolerance
        self.conf_natal_phase = cs.natal_phase
        self.conf_firdaria_night_order = cs.firdaria_night_order
        
    def load_data(self, ci):
        self.ci = ci
        swe_data = swissephData()
        i_date = ci.n_date.astimezone(pytz.utc)
        
        if type(ci.hsys) == type(u''):
            ci.hsys = ci.hsys.encode('ascii', 'ignore')

        self.result = swe_data.calc(ci.latitude, ci.longitude, i_date, ci.hsys)
        
        if ci.hsys == 'E':
            self.hsys_isequal = True
        else:
            self.hsys_isequal = False
        
        
        #根据conf 星体,显示相位，还有容许度
        bodies = [ i for i in self.result['bodies']\
                       if i['name'] in self.conf_natal_planets]
        houses = deepcopy(self.result['houses'])
        ascmcs = deepcopy(self.result['ascmcs'])
        
        
        if self.hsys_isequal == False:
            asc_deg = ascmcs[0]['degree_ut']
        else:
            asc_deg = ascmcs[0]['degree_ut'] + ascmcs[0]['degree']
        self.asc_deg = asc_deg #等宫制是上升点所在星座的头部位置
        
        #角度转换
        for body in bodies:
            #if 180 - body['degree_ut'] + asc_deg <= 360.0:
            #    body['degree_asc'] = 180 - body['degree_ut'] + asc_deg
            #else:
            #    body['degree_asc'] = -180 - body['degree_ut'] + asc_deg
            body['degree_asc'] = (180 - (body['degree_ut'] - asc_deg)) % 360
        
        for house in houses:
            #if 180 - house['degree_ut'] + asc_deg <= 360.0:
            #    house['degree_asc'] = 180 - house['degree_ut'] + asc_deg
            #else:
            #    house['degree_asc'] = -180 - house['degree_ut'] + asc_deg
            house['degree_asc'] = (180 - (house['degree_ut'] - asc_deg)) % 360
            
        for ascmc in ascmcs:
            #if 180 - ascmc['degree_ut'] + asc_deg <= 360.0:
            #    ascmc['degree_asc'] =  180 - ascmc['degree_ut'] + asc_deg
            #else:
            #    ascmc['degree_asc'] =  -180 - ascmc['degree_ut'] + asc_deg
            ascmc['degree_asc'] = (180 - (ascmc['degree_ut'] - asc_deg)) % 360
            
        #self赋值
        self.bodies = bodies
        self.houses = houses
        self.ascmcs = ascmcs
        self.aspects = []
        self.cal_aspects()
        #print self.aspects
        
    def cal_aspects(self):
        for body1 in self.bodies:
            for body2 in self.bodies:
                for type, delta in self.conf_natal_phase.iteritems(): #配置了哪些相位
                        #print type, delta
                        if body1['degree_ut'] <= body2['degree_ut']:
                            result = test_aspect(body1, body2, body1['degree_ut'],\
                                body2['degree_ut'], delta, self.conf_natal_tolerance[body1['name']],\
                                self.conf_natal_tolerance[body2['name']], type)
                            if not result == None:
                                aspect = { "name"    : type,
                                           "delta"   : delta,
                                           "body1"   : body1,
                                           "body1_name": body1['name'],
                                           "body2"   : body2,
                                           "body2_name": body2['name'],
                                           "degree1" : body1['degree_asc'],
                                           "degree2" : body2['degree_asc'],
                                           "angle"   : result[5]}
                                self.aspects.append(aspect)
        
    def render(self):
        tz = UserDefTZ(self.ci.n_tz)
        
        td = dict()
        td['qname'] = self.ci.qname
        td['location'] = self.ci.location
        td['latitude'] = self.ci.latitude
        td['longitude'] = self.ci.longitude
        td['date_str'] = self.ci.n_date.astimezone(tz).strftime('%Y-%m-%d %H:%M')
        td['tz_str'] = '+%.2f' % self.ci.n_tz
        
        
        r = 240.0
        td['c1'] = 'cx="240" cy="240" r="184"'
        td['c1style'] = 'fill: none; stroke: #ff0000; stroke-width: 1px; '
        td['c2'] = 'cx="240" cy="240" r="148"'
        td['c2style'] = 'fill: #fff; fill-opacity:.2; stroke: #ff0000; stroke-opacity:.4; stroke-width: 1px; '
        td['c3'] = 'cx="240" cy="240" r="128"'
        td['c3style'] = 'fill: #fff; fill-opacity:1; stroke: #ff0000; stroke-width: 1px; '
        
        #functions
        td['makeZodiac'] = self.make_zodiac( r )
        td['degreeRing'] = self.degree_ring( r )
        td['makeHouses'] = self.make_houses( r )
        td['makePlanets'] = self.make_planets( r )
        td['makeAspects'] = self.make_aspects( r )
        td['makeAspectGrid'] = self.make_aspectgrid()
#         td['makePlanetGrid'] = self.makePlanetGrid()
#         td['makeHousesGrid'] = self.makeHousesGrid()
        
        #通过模板生成svg
        f = codecs.open(NATAL_TEMPLATE_PATH, 'r', 'utf-8')
        template = Template(f.read()).substitute(td)
        f.close()
        return template
    
    def make_zodiac(self, r):  #星座
        svg_xml = ''
        
        if self.hsys_isequal:
            initD = - 180
        else:
            initD = - 180 + self.ascmcs[0]['degree']
        
        initS = self.ascmcs[0]['sign']

        step = 30.0 #每个星座30度
        style = 'fill:#ffffff; fill-opacity: 0.5;stroke: #000000; stroke-width: 1px'
        R = 184.0
        for i in range(12):
            nextD = initD - 30
            type = snames[initS]
            slice = '<path d="M' + str(r) + ',' + str(r) + ' L' + str(X1(initD, R, r)) + ',' + str(Y1(initD, R, r)) + \
            ' A' + str(R) + ',' + str(R) + ' 0 0,0 ' + str(X1(nextD, R, r)) + ',' + str(Y1(nextD, R, r)) + ' z" style="' + style + '"/>'
            sign = '<g transform="translate(-16,-16)"><use x="' + str(X1(initD-15, R-18, r)) + '" y="' + str(Y1(initD-15, R-18, r)) + '" xlink:href="#' + type + '" ></use></g>\n'
            svg_xml += slice + '\n' + sign
            initD = nextD
            initS = initS + 1
            if initS > 11:
                initS = 12 - initS
    
        return svg_xml
    
    def degree_ring(self, r): #每五度
        svg_xml = ''
        initD = - 180 + self.ascmcs[0]['degree']
        initS = self.ascmcs[0]['sign']
        step = 5.0 #每5度一个刻度
        R1 = 184
        R2 = 188
        for i in range(72):
            nextD = initD - 5.0
            x1 = X1(initD, R1, r)
            y1 = Y1(initD, R1, r)
            x2 = X1(initD, R2, r)
            y2 = Y1(initD, R2, r)
            svg_xml += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: #000; stroke-width: 1px; stroke-opacity:.9;"/>\n'\
                        % (x1,y1,x2,y2 )
            initD = nextD
        return svg_xml
    
    def make_houses(self, r):
        svg_xml = ''

        initD = 180
        R1 = 148
        R2 = 140
        linecolor ='orange'
        #print self.houses
        for i in range(12):
            initD = self.houses[i]['degree_asc']
            x1 = X1(initD, R1, r)
            y1 = Y1(initD, R1, r)
            if i < 11:
                nextD = self.houses[i+1]['degree_asc']
                if nextD == 0.0:
                    nextD = 360.0
            else:
                nextD = 180.0
            x2 = 240.0
            y2 = 240.0
            #midD = (initD+nextD)/2
            midD = circle_degree_mid(initD, nextD)
            #print i, initD, nextD, midD
            xtext = X1(midD, R2, r)
            ytext = Y1(midD, R2, r)
            slice = '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" style="stroke: '+linecolor+'; stroke-width: 2px; stroke-dasharray:3,2; stroke-opacity:.4;"/>\n'
            sign = '<text style="fill: #f00; fill-opacity: .6; font-size: 14px"><tspan x="'+str(xtext-3)+'" y="'+str(ytext+3)+'">'+str(i+1)+'</tspan></text>\n'
            svg_xml += slice + sign
            initD = self.houses[i]['degree_asc']
        return svg_xml
    
    def make_planets(self, r):
        svg_xml = ''
        
        body_rel_asc = deepcopy(self.bodies)
        body_rel_asc.sort(cmp_bodies)
        
        planet_drange = 3.4
        #找出聚集在一起的行星
        group_open=False
        groups = []
        for i, body in enumerate(body_rel_asc):
            if i == 0:
                prev = body_rel_asc[-1]
                next = body_rel_asc[1]
            elif i == (len(body_rel_asc)-1):
                prev = body_rel_asc[i-1]
                next = body_rel_asc[0]
            else:
                prev = body_rel_asc[i-1]
                next = body_rel_asc[i+1]
                
            diffa=degree_diff(prev['degree_asc'],body_rel_asc[i]['degree_asc'])
            diffb=degree_diff(next['degree_asc'],body_rel_asc[i]['degree_asc'])
            
            if (diffb < planet_drange):
                if group_open:
                    groups[-1].append([i,diffa,diffb, body_rel_asc[i]['name']])
                else:
                    group_open=True
                    groups.append([])
                    groups[-1].append([i,diffa,diffb, body_rel_asc[i]['name']])
            else:
                if group_open:
                    groups[-1].append([i,diffa,diffb, body_rel_asc[i]['name']])                
                group_open=False
            
        #print groups
        
        
        group_offset={}
        for i in range(len(body_rel_asc)):
            group_offset[i]=0.0
        #loop groups and set degrees display adjustment ***TODO怎么样把合相的分开画
        for i in range(len(groups)):
            if len(groups[i]) == 2:
                group_offset[groups[i][0][0]]=1.0
                group_offset[groups[i][1][0]]=-1.0
            elif len(groups[i]) == 3:
                group_offset[groups[i][0][0]]=1.5
                group_offset[groups[i][1][0]]=0
                group_offset[groups[i][2][0]]=-1.5
            elif len(groups[i]) == 4:
                group_offset[groups[i][0][0]]=2.0
                group_offset[groups[i][1][0]]=1.0
                group_offset[groups[i][2][0]]=-1.0
                group_offset[groups[i][3][0]]=-2.0
                
        for i, body in enumerate(body_rel_asc):
            #line1
            R1 = 128
            R2 = 184
            R3 = 220
            R4 = 240
            x1 = X1(body['degree_asc'], R1, r)
            y1 = Y1(body['degree_asc'], R1, r)
            x2 = X1(body['degree_asc'], R2, r)
            y2 = Y1(body['degree_asc'], R2, r)
            line1 = '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" style="stroke: '+'black'+'; stroke-width: 1px; stroke-opacity:.5;"/>\n'
            #line2
            offset = 0.0
            try:
                offset = group_offset[i]
            except KeyError:
                offset = 0.0
                
            x1 = x2
            y1 = y2
            x2 = X1(body['degree_asc']+offset, R3, r)
            y2 = Y1(body['degree_asc']+offset, R3, r)
            line2 = '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" style="stroke: '+'black'+'; stroke-width: 2px; stroke-opacity:.6;"/>\n'
            
            #planet
            planet_x = X1(body['degree_asc']+offset, R4, r)
            planet_y = Y1(body['degree_asc']+offset, R4, r)
            scale=1
            planet_xml = '<g transform="translate(-'+str(12*scale)+',-'+str(12*scale)+')"><g transform="scale('+str(scale)+')"><use x="' \
            + str(planet_x*(1/scale)) + '" y="' + str(planet_y*(1/scale)) + '" xlink:href="#' + body_rel_asc[i]['name'] + '" ></use></g></g>\n'
            
            svg_xml += line1 + line2 + planet_xml
        
        return svg_xml
        
    def make_aspects(self, r):
        svg_xml = ''

        for aspect in self.aspects:
            R1 = 128
            x1 = X1(aspect['body1']['degree_asc'], R1, r)
            y1 = Y1(aspect['body1']['degree_asc'], R1, r)
            x2 = X1(aspect['body2']['degree_asc'], R1, r)
            y2 = Y1(aspect['body2']['degree_asc'], R1, r)
            color = aspect_rel_color[aspect['name']]
            line = '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" style="stroke: '+color+'; stroke-width: 1; stroke-opacity: .9;"/>\n'
            svg_xml += line
        
        return svg_xml
    
    def make_aspectgrid(self):
        aspects = self.aspects
        out=""
        style='stroke:#000; stroke-width: 1px; stroke-opacity:.6; fill:none'
        xindent=380
        yindent=468
        box=14
        revr=range(len(self.conf_natal_planets))
        revr.reverse()
        for a in revr:
            start=self.conf_natal_planets[a]
            #first planet 
            out = out + '<rect x="'+str(xindent)+'" y="'+str(yindent)+'" width="'+str(box)+'" height="'+str(box)+'" style="'+style+'"/>\n'
            out = out + '<use transform="scale(0.4)" x="'+str((xindent+2)*2.5)+'" y="'+str((yindent+1)*2.5)+'" xlink:href="#'+start+'" ></use>\n'
            xindent = xindent + box
            yindent = yindent - box
            revr2=range(a)
            revr2.reverse()
            xorb=xindent
            yorb=yindent + box
            for b in revr2:
                end = self.conf_natal_planets[b]
                has_aspect = False
                aspect_start_end = None
                for aspect in aspects:
                    if start == aspect['body1_name'] and end == aspect['body2_name']:
                        has_aspect = True
                        aspect_start_end = aspect
                    if start == aspect['body2_name'] and end == aspect['body1_name']:
                        has_aspect = True
                        aspect_start_end = aspect
                        
                out = out + '<rect x="'+str(xorb)+'" y="'+str(yorb)+'" width="'+str(box)+'" height="'+str(box)+'" style="'+style+'"/>\n'
                xorb=xorb+box
                if has_aspect == True:
                    #print aspect_start_end
                    out = out + '<use  x="'+str(xorb-box+1)+'" y="'+str(yorb+1)+'" xlink:href="#'+aspect_rel_symbol[aspect_start_end['name']]+'" ></use>\n'
        
        return out
    
    def calc_planet_table_data(self):        
        #1.计算宫位的区间
        houses_info = list()
        htable_data = list()
        for i, house in enumerate(self.houses):
            house_info = dict()
            table_row = dict()
            house_info['id']=i+1
            j = (i+1)%12
            house_info["start_degree"]=self.houses[i]["degree"]
            house_info["end_degree"]=self.houses[j]["degree"]
            house_info["start_degree_asc"]=self.houses[i]["degree_asc"]
            house_info["end_degree_asc"]=self.houses[j]["degree_asc"]
            house_info["start_zodiac"]=self.houses[i]["sign"]
            house_info["end_zodiac"]=self.houses[j]["sign"]
            
            #判断是否有劫夺的情况
            if self.houses[j]["sign"] == (self.houses[i]["sign"]+2)%12:
                house_info["is_rob"] = True
                house_info["rob_zodiac"] = (self.houses[i]["sign"]+1)%12
            else:
                house_info["is_rob"] = False
                house_info["rob_zodiac"] = None
            
            house_info["ruler"] = list()
            house_info["ruler"].append(ruler_of_zodiac[house_info["start_zodiac"]]["ruler"])
            if house_info["is_rob"] == True:
                house_info["ruler"].append(ruler_of_zodiac[house_info["rob_zodiac"]]["ruler"])
            
            house_info["exalt"] = list()
            if not ruler_of_zodiac[i]["ruler"] == None:
                house_info["exalt"].append(ruler_of_zodiac[house_info["start_zodiac"]]["exalt"])
            
            houses_info.append(house_info)
            
            table_row["id"] = i+1
            table_row["longitude_svg"] = svg_symbol(snames[house_info["start_zodiac"]])
            table_row["longitude_str"] = dec2deg(house_info["start_degree"], type='2')
            table_row["ruler"] = [svg_symbol(ruler) for ruler in house_info["ruler"]]
            table_row["exalt"] = [svg_symbol(exalt) for exalt in house_info["exalt"]]
            htable_data.append(table_row)
        
        #2.计算行星庙旺落陷得分
        ptable_data = list()
        rtable_data = list()
        for body in self.bodies:
            table_row = dict()
            
            #body
            body_name = body["name"]
            body_svg = svg_symbol(body_name)
            zodiac_id = body["sign"]
            
            #longitude
            longitude_svg = svg_symbol(snames[body['sign']])
            longitude_degree = body['degree']
            longitude_str = dec2deg(body['degree'],type='2')
            longitude_rx = body['retrograde'] #是否逆行
            
            house_id = 12
            rule_house = list()
            exalt_house = list()
            for house_info in houses_info:
                if body["degree_asc"] <= house_info["start_degree_asc"] and \
                    body["degree_asc"] > house_info["end_degree_asc"]:
                    house_id = house_info["id"]
                if body["name"] in house_info["ruler"]:
                    rule_house.append(house_info["id"])
                if body["name"] in house_info["exalt"]:
                    exalt_house.append(house_info["id"])
            
            #print rule_house
            #print exalt_house
            
            is_ruler = False
            is_exalt = False
            is_detr = False
            is_fall = False
            is_triple = False
            is_term = False
            is_face = False

            if body_name == ruler_of_zodiac[zodiac_id]["ruler"]:
                is_ruler = True
            else:
                is_ruler = False
            if body_name == ruler_of_zodiac[zodiac_id]["exalt"]:
                is_exalt = True
            else:
                is_exalt = False
            if body_name == ruler_of_zodiac[zodiac_id]["fall"]:
                is_fall = True
            else:
                is_fall = False
            if body_name == ruler_of_zodiac[zodiac_id]["detr"]:
                is_detr = True
            else:
                is_detr = False

            if body_name in triple_of_zodiac[zodiac_id]["triple"]:
                is_triple = True
            else:
                is_triple = False
            
            term_p = None
            for term in term_of_zodiac[zodiac_id]["term"]:
                if longitude_degree >= term[0] and \
                    longitude_degree < term[1]:
                    term_p = term[2]
                    #print body, term_p, zodiac_id
                    if body_name == term[2]:
                        is_term = True
            
            face_p = None
            for face in face_of_zodiac[zodiac_id]["face"]:
                if longitude_degree >= face[0] and \
                    longitude_degree < face[1]:
                    face_p = face[2]
                    #print body, face_p, zodiac_id
                    if body_name == face[2]:
                        is_face = True
                        
            ruler_p = ruler_of_zodiac[zodiac_id]["ruler"]
            exalt_p = ruler_of_zodiac[zodiac_id]["exalt"]
            fall_p = ruler_of_zodiac[zodiac_id]["fall"]
            detr_p = ruler_of_zodiac[zodiac_id]["detr"]
            triple_p = triple_of_zodiac[zodiac_id]["triple"]

            score = 0
            if is_ruler:
                score = score + 5
            if is_exalt:
                score = score + 4
            if is_triple:
                score = score + 3
            if is_term:
                score = score + 2
            if is_face:
                score = score + 1
            if is_fall:
                score = score - 4
            if is_detr:
                score = score - 5
            
            if body_name not in bnames_small:
                score = None
                
            table_row["body"] = body
            table_row["body_svg"] = body_svg
            table_row["longitude_svg"] = longitude_svg
            table_row["longitude_degree"] = longitude_degree
            table_row["longitude_str"] = longitude_str
            table_row["longitude_rx"] = longitude_rx
            table_row["house_id"] = house_id
            table_row["rule_house"] = rule_house
            table_row["exalt_house"] = exalt_house
            table_row["is_ruler"] = is_ruler
            table_row["is_exalt"] = is_exalt
            table_row["is_detr"] = is_detr
            table_row["is_fall"] = is_fall
            table_row["is_triple"] = is_triple
            table_row["is_term"] = is_term
            table_row["is_face"] = is_face
            table_row["ruler"] = ruler_p
            table_row["exalt"] = exalt_p
            table_row["detr"] = detr_p
            table_row["fall"] = fall_p
            table_row["triple"] = triple_p
            table_row["term"] = term_p
            table_row["face"] = face_p
            table_row["score"] = score

            ptable_data.append(table_row)
        
        
        #3.判断接纳和互溶
        for i, body_one in enumerate(self.bodies):

            if body_one["name"] not in bnames_small:
                continue
            
            body1 = body_one["name"]
            #print u"计算互溶"
            #print body1

            ruler_p = ptable_data[i]["ruler"]
            exalt_p = ptable_data[i]["exalt"]
            
            triple_p = ptable_data[i]["triple"]
            term_p = ptable_data[i]["term"]
            face_p = ptable_data[i]["face"]
            
            #print triple_p
            #print term_p
            #print face_p
            
            two_in_trip_term_face = False
            planet_in_trip_term_face = []
            #pattern_in_trip_term_face = ""
            
            if term_p == face_p:
                two_in_trip_term_face = True
                if term_p in triple_p:
                    planet_in_trip_term_face.append((term_p, "Triple+Term+Face"))
                    #pattern_in_trip_term_face = "Triple+Term+Face"
                else:
                    planet_in_trip_term_face.append((term_p, "Term+Face"))
                    #pattern_in_trip_term_face = "Term+Face"
            else:
                    if term_p in triple_p:
                        two_in_trip_term_face = True
                        planet_in_trip_term_face.append((term_p, "Triple+Term"))
                        #pattern_in_trip_term_face = "Triple+Term"
        
                    if face_p in triple_p:
                        two_in_trip_term_face = True
                        planet_in_trip_term_face.append((face_p, "Triple+Face"))
                        #pattern_in_trip_term_face = "Triple+Face"
                        
            #print planet_in_trip_term_face
                

            for j, body_two in enumerate(self.bodies):
                if body_two["name"] not in bnames_small:
                    continue
                if j <= i:
                    continue
                
                body2 = body_two["name"]
                
                #body2的
                body2_index = j
                ruler_p2 = ptable_data[body2_index]["ruler"]
                exalt_p2 = ptable_data[body2_index]["exalt"]
                
                triple_p2 = ptable_data[body2_index]["triple"]
                term_p2 = ptable_data[body2_index]["term"]
                face_p2 = ptable_data[body2_index]["face"]
                
                
                two_in_trip_term_face_p2 = False
                planet_in_trip_term_face_p2 = []
                #pattern_in_trip_term_face_p2 = ""
                if term_p2 == face_p2:
                    two_in_trip_term_face_p2 = True
                    if term_p2 in triple_p2:
                        planet_in_trip_term_face_p2.append((term_p2,"Triple+Term+Face"))
                        #pattern_in_trip_term_face_p2 = "Triple+Term+Face"
                    else:
                        planet_in_trip_term_face_p2.append((term_p2,"Term+Face"))
                        #pattern_in_trip_term_face_p2 = "Term+Face"
                else:
                        if term_p2 in triple_p2:
                            two_in_trip_term_face_p2 = True
                            planet_in_trip_term_face_p2.append((term_p2,"Triple+Term"))
                            #pattern_in_trip_term_face_p2 = "Triple+Term"
                            
                        if face_p2 in triple_p2:
                            two_in_trip_term_face_p2 = True
                            planet_in_trip_term_face_p2.append((face_p2,"Triple+Face"))
                            #pattern_in_trip_term_face_p2 = "Triple+Face"
                    

                    
                
                
                #判断互溶
                rtable_row = dict()
                is_mutual = False
                #本垣 和 三分-界-十度取二
                #耀升 和  三分-界-十度取二
                #三分-界-十度取二 和 三分-界-十度取二
                for (trip_term_face, pattern) in planet_in_trip_term_face:
                    if trip_term_face == body2:
                        if ruler_p2 == body1:
                            is_mutual = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "mutual"
                            rtable_row["body1_pattern"] = "ruler"
                            rtable_row["body2_pattern"] = pattern
                            rtable_data.append(rtable_row)
                    if trip_term_face == body2:
                        if exalt_p2 == body1:
                            is_mutual = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "mutual"
                            rtable_row["body1_pattern"] = "exalt"
                            rtable_row["body2_pattern"] = pattern
                            rtable_data.append(rtable_row)
                    for (trip_term_face_p2, pattern_p2) in planet_in_trip_term_face_p2:
                        if trip_term_face == body2 and trip_term_face_p2 == body1:
                            is_mutual = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "mutual"
                            rtable_row["body1_pattern"] = pattern_p2
                            rtable_row["body2_pattern"] = pattern
                            rtable_data.append(rtable_row)
                        
                
                #本垣 和 耀升，
                #耀升 和 耀升
                #三分-界-十度取二 和 耀升
                rtable_row = dict()
                if exalt_p == body2:
                    if ruler_p2 == body1:
                        is_mutual = True
                        rtable_row = dict()
                        rtable_row["body1"] = body1
                        rtable_row["body2"] = body2
                        rtable_row["pattern"] = "mutual"
                        rtable_row["body1_pattern"] = "ruler"
                        rtable_row["body2_pattern"] = "exalt"
                        rtable_data.append(rtable_row)
                    if exalt_p2 == body1:
                        is_mutual = True
                        rtable_row = dict()
                        rtable_row["body1"] = body1
                        rtable_row["body2"] = body2
                        rtable_row["pattern"] = "mutual"
                        rtable_row["body1_pattern"] = "exalt"
                        rtable_row["body2_pattern"] = "exalt"
                        rtable_data.append(rtable_row)
                    for (trip_term_face_p2, pattern_p2) in planet_in_trip_term_face_p2:
                        if trip_term_face_p2 == body1:
                            is_mutual = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "mutual"
                            rtable_row["body1_pattern"] = "exalt"
                            rtable_row["body2_pattern"] = pattern_p2
                            
                            rtable_data.append(rtable_row)
                    
                
                #三分-界-十度取二 和  本垣 ， 
                #本垣 和 本垣，
                #耀升 和 本垣
                rtable_row = dict()
                if ruler_p == body2:
                    for (trip_term_face_p2, pattern_p2) in planet_in_trip_term_face_p2:
                        if trip_term_face_p2 == body1:
                            is_mutual = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "mutual"
                            rtable_row["body1_pattern"] = pattern_p2
                            rtable_row["body2_pattern"] = "ruler"
                            rtable_data.append(rtable_row)
                    if ruler_p2 == body1:
                        is_mutual = True
                        rtable_row = dict()
                        rtable_row["body1"] = body1
                        rtable_row["body2"] = body2
                        rtable_row["pattern"] = "mutual"
                        rtable_row["body1_pattern"] = "ruler"
                        rtable_row["body2_pattern"] = "ruler"
                        rtable_data.append(rtable_row)
                    if exalt_p2 == body1:
                        is_mutual = True
                        rtable_row = dict()
                        rtable_row["body1"] = body1
                        rtable_row["body2"] = body2
                        rtable_row["pattern"] = "mutual"
                        rtable_row["body1_pattern"] = "exalt"
                        rtable_row["body2_pattern"] = "ruler"
                        rtable_data.append(rtable_row)
                
                if is_mutual == True:
                    #rtable_data.append(rtable_row)
                    #print rtable_data
                    pass
                
                #判断接纳
                #body1 被 body2 接纳——body1跑到body2的国家
                is_respect = False
                if is_mutual == False:
                    has_aspect = False
                    for aspect in self.aspects:
                        if body1 == aspect['body1_name'] and body2 == aspect['body2_name']:
                            has_aspect = True
                        if body1 == aspect['body2_name'] and body2 == aspect['body1_name']:
                            has_aspect = True
                    if has_aspect == True:
                        #print body1, body2, planet_in_trip_term_face
                        for (trip_term_face, pattern) in planet_in_trip_term_face:
                            if trip_term_face == body2:
                                is_respect = True
                                rtable_row = dict()
                                rtable_row["body1"] = body1
                                rtable_row["body2"] = body2
                                rtable_row["pattern"] = "respect"
                                rtable_row["body1_pattern"] = pattern
                                rtable_row["body2_pattern"] = ""
                                rtable_data.append(rtable_row)
                        if exalt_p == body2:
                            is_respect = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "respect"
                            rtable_row["body1_pattern"] = "exalt"
                            rtable_row["body2_pattern"] = ""
                            rtable_data.append(rtable_row)
                        if ruler_p == body2:
                            is_respect = True
                            rtable_row = dict()
                            rtable_row["body1"] = body1
                            rtable_row["body2"] = body2
                            rtable_row["pattern"] = "respect"
                            rtable_row["body1_pattern"] = "ruler"
                            rtable_row["body2_pattern"] = ""
                            rtable_data.append(rtable_row)
                        
                        for (trip_term_face_p2, pattern) in planet_in_trip_term_face_p2:
                            if trip_term_face_p2 == body1:
                                is_respect = True
                                rtable_row = dict()
                                rtable_row["body1"] = body2
                                rtable_row["body2"] = body1
                                rtable_row["pattern"] = "respect"
                                rtable_row["body1_pattern"] = pattern
                                rtable_row["body2_pattern"] = ""
                                rtable_data.append(rtable_row)
                        if exalt_p2 == body1:
                            is_respect = True
                            rtable_row = dict()
                            rtable_row["body1"] = body2
                            rtable_row["body2"] = body1
                            rtable_row["pattern"] = "respect"
                            rtable_row["body1_pattern"] = "exalt"
                            rtable_row["body2_pattern"] = ""
                            rtable_data.append(rtable_row)
                        if ruler_p2 == body1:
                            is_respect = True
                            rtable_row = dict()
                            rtable_row["body1"] = body2
                            rtable_row["body2"] = body1
                            rtable_row["pattern"] = "respect"
                            rtable_row["body1_pattern"] = "ruler"
                            rtable_row["body2_pattern"] = ""
                            rtable_data.append(rtable_row)
                    if is_respect == True:
                        #rtable_data.append(rtable_row)
                        #print rtable_data
                        pass
        
        for table_row in rtable_data:
            table_row["body1_svg"] = svg_symbol(table_row["body1"])
            table_row["body2_svg"] = svg_symbol(table_row["body2"])
        return (ptable_data, htable_data, rtable_data)
    
    def firdaria(self):
        firdaria_order_day = ["sun","venus","mercury","moon","saturn","jupiter",\
                              "mars","mean node","south node"]
        firdaria_order_night0 = ["moon","saturn","jupiter","mars","mean node",\
                                 "south node","sun","venus", "mercury"]
        firdaria_order_night1 = ["moon","saturn","jupiter","mars","sun","venus",\
                                 "mercury","mean node","south node"]
        
        #每颗行星掌管年限
        planet_rule_year = {"sun":10,"moon":9,"saturn":11,"jupiter":12,"mars":7,\
                            "venus":8,"mercury":13,"mean node":3,"south node":2}
        
        #子限
        planet_sub_order = {"sun":["sun","venus","mercury","moon","saturn","jupiter","mars"],
                            "venus":["venus","mercury","moon","saturn","jupiter","mars","sun"],
                            "mercury":["mercury","moon","saturn","jupiter","mars","sun","venus"],
                            "moon":["moon","saturn","jupiter","mars","sun","venus","mercury"],
                            "saturn":["saturn","jupiter","mars","sun","venus","mercury","moon"],
                            "jupiter":["jupiter","mars","sun","venus","mercury","moon","saturn"],
                            "mars":["mars","sun","venus","mercury","moon","saturn","jupiter"]
                            }
        
        #1.判断是昼生人还是夜生人
        birth_on_day = True
        for body1 in self.bodies:
            if body1['name'] == "sun":
                #print body1['degree_asc']
                if body1['degree_asc'] >= 0 and body1['degree_asc'] <= 180:
                    birth_on_day = False
        
        if birth_on_day == True:
            firdaria_order = firdaria_order_day
        else:
            if self.conf_firdaria_night_order == 0:
                firdaria_order = firdaria_order_night0
            else:
                firdaria_order = firdaria_order_night1
        
        #2.按顺序排 每颗行星
        firdaria_result = []
        tz = UserDefTZ(self.ci.n_tz)
        begindt = self.ci.n_date.astimezone(tz)
        enddt = None
        first_in_nodes = True
        for p in firdaria_order:
            p_rule_year = planet_rule_year[p]
            enddt =  begindt + relativedelta(years=p_rule_year)
            sub_unit = (enddt-begindt)/7 #7颗行星
            if not p == "mean node" and not p == "south node":
                firdaria_planet = []
                for sub_index, sub_p in enumerate(planet_sub_order[p]):
                    firdaria_row = dict()
                    firdaria_row["main"] = p
                    firdaria_row["main_svg"] = svg_symbol(p)
                    firdaria_row["sub"] = sub_p
                    firdaria_row["sub_svg"] = svg_symbol(sub_p)
                    sub_begindt = begindt + sub_index*sub_unit
                    firdaria_row["begindt"] = sub_begindt
                    firdaria_planet.append(firdaria_row)
                firdaria_result.append(firdaria_planet)
            else:
                if first_in_nodes == True:
                    firdaria_planet = []
                
                firdaria_row = dict()
                firdaria_row["main"] = p
                firdaria_row["main_svg"] = svg_symbol(p)
                firdaria_row["sub"] = ''
                firdaria_row["sub_svg"] = ''
                firdaria_row["begindt"] = begindt
                firdaria_planet.append(firdaria_row)
                if first_in_nodes == False:
                    firdaria_result.append(firdaria_planet)
                first_in_nodes = False
                
            begindt = enddt
        
        return firdaria_result
        
        
        