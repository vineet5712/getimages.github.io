from django.urls import path
from . import views

urlpatterns = [
    path('', views.showData, name='showData'),
    path('hlo/', views.ApiData, name='ApiData'),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('addApiData/', views.addApiData, name='addApiData'),
]