from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('link/', views.link, name='link'),
    path('link/<str:link_path>/', views.link_detail, name='link_detail'),
    path('link/<str:link_path>/customer/', views.customer, name='customer'),
    path('id_card_ocr/', views.id_card_ocr, name='id_card_ocr'),
]
