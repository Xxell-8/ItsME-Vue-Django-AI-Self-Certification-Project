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
    path('partner/getuser/', views.get_user, name='get_user')
]
