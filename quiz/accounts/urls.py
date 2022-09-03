from django.contrib import admin
from django.urls import path,include,re_path as url

from . import views
from accounts.views import(
    register_view,
    home,
)
urlpatterns = [
    # path('register/',views.register_view),
    path('logout/',views.logout_view),
    path('login/',views.loginSigninController,name="context"),

    path('otpverification/',views.otpverification,name="otp"),
    # url(r'^otpverification/', views.otpverification, name = 'otp')


]

