from django.db import models
from django_mysql.models import ListTextField

class CarRTO(models.Model):

    # Fields
    Brand = models.CharField(max_length=20, null = False, blank = False)
    Owner = models.CharField(max_length=30, null = False, blank = False)
    DateRegistered = models.DateTimeField()
    CarModel = models.CharField(max_length=20, null = False, blank = False)
    PlateNumber = models.CharField(max_length=20, unique = True, primary_key = True,  null = False, blank  = False)
    CrimeRecord = models.CharField(max_length = 1000, null = True)
    LastPollutionCheck = models.DateTimeField()
    LastInsuranceRenew = models.DateTimeField()

    def __str__(self):
        return str(self.pk)


class CarSurveillance(models.Model):

    # Fields
    Color = models.CharField(max_length=10)
    CarModel = models.CharField(max_length=20)
    PlateNumber = models.CharField(max_length=20, null = False, blank = False)
    Brand = models.CharField(max_length=20)
    CameraID = models.CharField(max_length = 10, null=False, blank=False)
    Imagename= models.CharField(max_length = 20)
    VideoTimeStamp = models.CharField(max_length = 20)
    VideoFPS = models.IntegerField(default=60)
    Videoname = models.CharField(max_length = 20)
    Seen = models.DateTimeField(editable = True)


    def __str__(self):
        return str(self.pk)

class Camera(models.Model):

    # Fields
    Location = models.TextField(max_length=100)
    CameraID = models.CharField(max_length = 20, primary_key=True)
    X_coordinate = models.IntegerField()
    Y_coordinate = models.IntegerField()

    def __str__(self):
        return str(self.pk)


class Person(models.Model):
    
    ImageName = models.CharField(max_length = 20)
    Address = models.TextField()
    CrimeRecord = models.TextField()
    IsLicensed = models.BooleanField()
    Name = models.CharField(max_length = 20)
    VehiclesRegistered =  ListTextField( base_field=models.CharField(max_length = 20),size=10)
    PersonId = models.CharField(max_length = 20, primary_key = True)

    def __str__(self):
        return str(self.pk)