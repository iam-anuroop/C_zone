from django.contrib import admin
from .models import HotelDetails

# Register your models here.

class HoteldetailsAdmin(admin.ModelAdmin):
    list_display = ('hotel_id','hotel_name','hotel_location')
admin.site.register(HotelDetails,HoteldetailsAdmin)