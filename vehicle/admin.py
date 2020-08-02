from django.contrib import admin
from .models import   Camera, CarSurveillance, CarRTO, Person



admin.site.register(CarSurveillance)
admin.site.register(CarRTO)
admin.site.register(Camera)
admin.site.register(Person)