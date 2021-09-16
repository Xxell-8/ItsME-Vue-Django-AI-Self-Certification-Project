from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('link/', views.link, name='link'),
    path('link/<int:link_id>/', views.link_detail, name='link_detail'),
    path('link/<int:link_id>/client/', views.client, name='client'),
    path('template/', views.template, name='template'),
    path('template/<int:template_id>/', views.template_detail, name='template_detail'),
]
