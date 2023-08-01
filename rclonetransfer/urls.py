from django.urls import path
from .views import HomeView, LoginView, RegisterUserView, GoogleFormView, DropboxFormView, ChooseFoldersView, RCloneButtonView, RCloneJobView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from .dropbox import DropboxLoginView, DropboxCallbackView
from .google import GoogleLoginView, GoogleCallbackView
from . import views


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('googleform/', GoogleFormView.as_view(), name='googleform'),
    path('dropboxform/', DropboxFormView.as_view(), name='dropboxform'),
    path('google/login/', GoogleLoginView.as_view(), name='google-login'),
    path('google/callback/', GoogleCallbackView.as_view(), name='google-callback'),
    path('dropbox/login/', DropboxLoginView.as_view(), name='dropbox-login'),
    path('dropbox/callback/', DropboxCallbackView.as_view(), name='dropbox-callback'),
    path('choose-folders/', ChooseFoldersView.as_view(), name='choose-folders'),
    path('accounts/profile/', RedirectView.as_view(url='/'), name='account_redirect'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('rclone_job_view/', views.RCloneJobView.as_view(), name='rclone_job_view'),
    path('rclonebutton/', RCloneButtonView.as_view(), name='rclonebutton'),
]