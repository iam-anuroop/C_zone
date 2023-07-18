from django.contrib import admin
from .models import HotelDetails,Roomtype

# Register your models here.

class HoteldetailsAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_name','hotel_email','last_login', 'date_joined')
admin.site.register(HotelDetails,HoteldetailsAdmin)

class RoomtypeAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_id','roomtype','created_at','updated_at')
admin.site.register(Roomtype,RoomtypeAdmin)