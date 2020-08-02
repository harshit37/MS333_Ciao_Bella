from django.urls import path
from . import views


urlpatterns = [
    path('', views.save_to_database, name = 'save_to_database'),
    path('querybyimage', views.querybyimage, name = 'querybyimage'),
    path('querybyform', views.querybyform, name = 'querybyform'),
    path('videoplayer', views.video_player,name = 'videoplayer'),
    path('savetodatabase', views.savetodatabase, name = 'savetodatabase'),
    path('testingpage', views.testingpage, name = 'testingpage') 
]