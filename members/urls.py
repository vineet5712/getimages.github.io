from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.showData, name='showData'),
    path('hlo/', views.ApiData, name='ApiData'),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('addApiData/', views.addApiData, name='addApiData'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)