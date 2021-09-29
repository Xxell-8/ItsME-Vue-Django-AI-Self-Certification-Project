from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('link/', views.link, name='link'),
    path('link/<int:link_id>/', views.link_detail, name='link_detail'),
    path('link/<int:link_id>/customer/', views.customer, name='customer'),
    path('id_card_ocr/', views.id_card_ocr, name='id_card_ocr'),
]
