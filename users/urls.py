from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from users import views


urlpatterns = [

    path("accounts/", views.UserView.as_view()),
    path("accounts/newest/<int:num>/", views.UserDetailView.as_view()),
    path("login/", ObtainAuthToken.as_view()),
]
