# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
import base64
import pickle
from utils import ChartSetsNoModel

GENDER_CHOICES = (
    ('M', '男'),
    ('F', '女'),
    ('U', '未知')
)
CHART_TYPE_CHOICES = (
    ('N', '本命盘'),
    ('T', '流年盘')
)
ISPUB_CHOICES = (
    ('N','不公开'),
    ('Y', '公开')
)
HSYS_CHOICES = (
    ('P','Placidus 普拉西分宫制'),
    ('E', 'Equal 等宫制'),
    ('B', 'Alcabitus 阿卡比特分宫制')
)

#natal
class ChartInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qname = models.CharField(max_length=200)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                                      default='U')
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    n_date = models.DateTimeField()
    n_tz = models.FloatField()
    hsys = models.CharField(max_length=2, choices=HSYS_CHOICES, default='B')
    chart_type = models.CharField(max_length=2, choices=CHART_TYPE_CHOICES, default='N')
    t_date = models.DateTimeField(null=True, blank=True)
    is_pub = models.CharField(max_length=2, default='N', choices=ISPUB_CHOICES)
    update_time = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)
    pubnote = models.TextField(null=True, blank=True)

class ChartInfoForm(ModelForm):
    n_date = forms.DateTimeField(input_formats=("%Y-%m-%d %H:%M:%S",))
    t_date = forms.DateTimeField(input_formats=("%Y-%m-%d %H:%M:%S",), required=False)
    #gender = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"gender"},choices=GENDER_CHOICES))
    #hsys = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"hsys"}))
    #chart_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"chart_type"}))
    #is_pub = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"is_pub"}))
    
    class Meta:
        model = ChartInfo
        widgets = {
            'gender': forms.Select(attrs={"class":"form-control", "id":"gender"}),
            'hsys': forms.Select(attrs={"class":"form-control", "id":"hsys"}),
            'chart_type': forms.Select(attrs={"class":"form-control", "id":"chart_type"}),
            'is_pub': forms.Select(attrs={"class":"form-control", "id":"is_pub"})
        }
    
class ChartSets(models.Model):
    id = models.AutoField(primary_key=True)
    natal_planets_char = models.CharField(max_length=1000)
    natal_tolerance_char = models.CharField(max_length=1000)
    natal_phase_char = models.CharField(max_length=1000)
    transit_planet_char = models.CharField(max_length=1000)
    transit_tolerance_char = models.CharField(max_length=1000)
    transit_phase_char = models.CharField(max_length=1000)
    firdaria_set = models.CharField(max_length=1000)
    
    
    @property
    def natal_planets(self):
        data = base64.b64decode(self.natal_planets_char)
        natal_planets = pickle.loads(data)
        return natal_planets
    
    @property
    def natal_tolerance(self):
        data = base64.b64decode(self.natal_tolerance_char)
        natal_tolerance = pickle.loads(data)
        return natal_tolerance
    
    @property
    def natal_phase(self):
        data = base64.b64decode(self.natal_phase_char)
        natal_phase = pickle.loads(data)
        return natal_phase
    
    @property
    def transit_planet(self):
        data = base64.b64decode(self.trasit_planet_char)
        trasit_planet = pickle.loads(data)
        return trasit_planet
    
    @property
    def transit_tolerance(self):
        data = base64.b64decode(self.trasit_tolerance_char)
        trasit_tolerance = pickle.loads(data)
        return trasit_tolerance
    
    @property
    def transit_phase(self):
        data = base64.b64decode(self.trasit_phase_char)
        trasit_phase = pickle.loads(data)
        return trasit_phase
    
    
default_chartsets = ChartSetsNoModel()

default_chartsets.natal_planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "mean node", "Asc", "Mc"]

default_chartsets.natal_tolerance = {"sun":15, "moon":12, "mercury":7, "venus":7, "mars":8,\
                                     "jupiter":9, "saturn":9, "mean node":5, "Asc":0, "Mc":0}

default_chartsets.natal_phase = {"conjunction":0, "sextile":60, "square":90, "trine":120, "opposition":180}

default_chartsets.transit_planet = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",\
                    "uranus", "neptune", "pluto", "mean node"]

default_chartsets.transit_tolerance = {"sun":3, "moon":3, "mercury":3, "venus":3, "mars":3, "jupiter":3, "saturn":3,\
                    "uranus":3, "neptune":3, "pluto":3, "mean node":3, "Asc":3, "Mc":3}

default_chartsets.transit_phase = {"conjunction":0, "semi-square":45, "sextile":60, "square":90,\
                                   "trine":120, "sesquiquadrate":135, "quincunx":150, "opposition":180}

default_chartsets.firdaria_night_order = 0

def getChartSets(user):
    try:
        charsets = ChartSets.objects.get(user=user)
    except:
        return default_chartsets
