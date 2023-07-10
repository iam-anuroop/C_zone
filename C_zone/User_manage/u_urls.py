from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='registration'),
    path('login/',views.login_view,name='login'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('emailnotification',views.emailnotification,name='emailnotification'),
    path('resetpassword/<uidb64>/<token>/',views.resetpasswordorusername,name='resetpassword'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    ]
