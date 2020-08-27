from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from authentication import views

router = DefaultRouter()

urlpatterns = [
    url(r'^login/', views.LoginView.as_view()), #views.obtain_jwt_token
    url(r'^logout/', views.LogoutView.as_view()), #refresh_jwt_token
    url(r'^token/refresh/', refresh_jwt_token),
    url(r'^token/verify/', verify_jwt_token),
    url(r'^profile/(?P<pk>[0-9]+)/', views.ProfileDetail.as_view()),
    url(r'^profile/change_password/(?P<pk>[0-9]+)/', views.ChangePasswordView.as_view()),
]
