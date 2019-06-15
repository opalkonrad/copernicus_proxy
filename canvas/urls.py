from django.urls import path

from . import views

urlpatterns = [
    path('copernicus/', views.CopernicusView.as_view(), name='copernicus'),
    path('db_browser/', views.DatabaseBrowser.as_view(), name='db_browser')
]
