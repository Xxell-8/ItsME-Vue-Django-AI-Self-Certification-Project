from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('partner/', views.partner, name='partner'),
    path('partner/auth/', views.partner_auth, name='partner_auth'),
    path('partner/approval/', views.approval, name='approval'),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('changepwd/<str:username>/', views.changepwd, name='changepwd'),
    path('findpwd/', views.findpwd, name='findpwd'),
]
