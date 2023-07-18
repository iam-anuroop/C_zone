from django.urls import path
from . import views

urlpatterns = [
    path('',views.Hotelregister,name='hotelregistration'),
    path('activatehotel/<uidb64>/<token>/',views.activatehotel,name='activatehotel'),
    path('hotel_login/',views.Hotellogin,name='hotellogin'),
    path('hotel_home/',views.Hotelhome,name='hotelhome'),
    path('hotel_logout/',views.Hotellogout,name='hotellogout'),
    path('roomtype/',views.Roomtype_view,name='roomtypeupdate'),
    path('hotelbook/<int:hotel_id>/',views.hotel_book,name='hotelbook'),
    ]
