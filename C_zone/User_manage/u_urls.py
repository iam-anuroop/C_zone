from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='registration'),
    path('login/',views.login_view,name='login'),
    ]
