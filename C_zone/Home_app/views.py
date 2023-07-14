from django.shortcuts import render , redirect 
from Hotel_manage.models import HotelDetails


def home(request):
    list_hotels = HotelDetails.objects.all()

    return render(request,'pages/home.html',{'hotels':list_hotels})

# Create your views here.
