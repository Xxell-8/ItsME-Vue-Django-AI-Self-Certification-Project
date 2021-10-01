from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('partner/', views.PartnerListAPIView.as_view(), name='partner'),
    path('partner/<int:pk>/', views.PartnerRegisterView.as_view(), name='partner'),
    path('partner/auth/', views.partner_auth, name='partner_auth'),
    path('profile/approval/<int:pk>/', views.UserApprovalView.as_view(), name='approval'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/update/<int:pk>/', views.UpdateProfileView.as_view(), name='updateprofile'),
    path('changepwd/<int:pk>/', views.ChangePasswordView.as_view(), name='changepwd'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('partner/getuser/', views.get_user, name='get_user'),
    path('pending/', views.pending, name='pending'),
    path('pending/<str:code>/', views.pending_list, name='pending_list'),
    path('count/', views.count, name='count'),
    path('count/<str:code>/', views.count_by_code, name='count_by_code'),
    path('getpartner/<str:code>/', views.get_partner, name='get_partner'),
    path('email/', views.email, name='email'),
]
