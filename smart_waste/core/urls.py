from django.urls import path
from .views import landing_page, about_view
from . import views

urlpatterns = [
    path('', landing_page, name='home'),
    path('about', about_view, name='about'),

    # User login & profile handling
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-reset/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    
    # Dashboard routes for different user types
    path('dashboard/public/', views.PublicDashboardView, name='public_dashboard'),
    path('dashboard/municipal/', views.municipal_dashboard, name='municipal_dashboard'),
    # path('dashboard/vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    
    # Profile routes
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]