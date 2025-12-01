from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/tasks/analyze/', views.analyze_tasks),
    path('api/tasks/suggest/', views.suggest_tasks),
]
