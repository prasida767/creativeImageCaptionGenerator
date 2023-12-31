from django.urls import path

from . import views

urlpatterns = [
    path("generate_caption", views.generate_caption, name="generate_caption"),
    path('list_models', views.list_models, name='list_models'),
]