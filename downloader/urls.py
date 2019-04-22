from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sea_level/', views.SeaLevelView.as_view(), name='sea_level')
]
