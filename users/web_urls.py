from django.urls import path
from django.contrib.auth import views as auth_views
from .web_views import SignupView, ProfileWebView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileWebView.as_view(), name='profile-web'),
]
