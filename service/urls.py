from django.urls import path

from . import views

urlpatterns = [
    path('tasks', views.TaskList.as_view(), name='task_list'),
    path('tasks/<int:task_id>', views.Task.as_view(), name='task'),
    # path('files/<int:file_id>', views.File.as_view(), name='file'),
    path('datasets', views.DataSetList.as_view(), name="dataset_list"),
    path('datasets/<int:dataset_id>', views.DataSet.as_view(), name='dataset'),
]
