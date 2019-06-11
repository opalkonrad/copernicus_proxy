from django.urls import path

from . import views

urlpatterns = [
    path('task', views.TaskList.as_view(), name='task_list'),
    path('task/<int:url_id>', views.Task.as_view(), name='task'),
    path('file/<int:url_id>', views.File.as_view(), name='file'),
    path('dataset', views.DataSetList.as_view(), name="dataset_list"),
    path('dataset/<int:url_id>', views.DataSet.as_view(), name='dataset'),
]
