from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('link/', views.link, name='link'),
    path('link/partner/<int:partner_id>/', views.link_count, name='link_count'),
    path('link/<str:link_path>/', views.link_detail, name='link_detail'),
    path('link/<str:link_path>/id_card_ocr/', views.id_card_ocr, name='id_card_ocr'),
    path('link/<str:link_path>/customer/', views.customer, name='customer'),
]
