from django.shortcuts import render , redirect 
from Hotel_manage.models import HotelDetails , Hotelowner


def home(request):
    list_hotels = HotelDetails.objects.all()
# 
    return render(request,'pages/home.html',{'hotels':list_hotels})


def Searchotel(request):

    if 'search' in request.GET:
        search = request.GET['search']
        list_hotels = HotelDetails.objects.filter(hotel_name__icontains = search)
    else:
        list_hotels = HotelDetails.objects.all()



    return render(request,'pages/home.html',{'hotels':list_hotels})
    

# Create your views here.
