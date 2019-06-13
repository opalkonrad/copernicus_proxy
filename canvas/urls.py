from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('copernicus/', views.CopernicusView.as_view(), name='canvas'),
    path('db_browser/', views.DatabaseBrowser.as_view(), name='db_browser'),
    path('testing/', views.TestView.as_view(), name='testing')
]
