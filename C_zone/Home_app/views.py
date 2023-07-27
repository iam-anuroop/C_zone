from django.shortcuts import render , redirect 
from Hotel_manage.models import HotelDetails , Roomtype
from django.db.models import Q


def home(request):

    # list_hotels = HotelDetails.objects.filter(is_registerd = True )
    id_hotels = Roomtype.objects.values_list('hotel_id', flat=True).distinct()
    list_hotels = HotelDetails.objects.filter(id__in = id_hotels,is_registerd = True,is_confirmed = True)

    return render(request,'pages/home.html',{'hotels':list_hotels})


def Searchotel(request):

    if 'search' in request.GET:
        search = request.GET['search']
        list_hotels = HotelDetails.objects.filter(Q(hotel_name__icontains=search) | Q(city__icontains=search) | Q(state__icontains=search))

        return render(request,'pages/home.html',{'hotels':list_hotels})
    else:
        list_hotels = HotelDetails.objects.all()
        return render(request,'pages/home.html',{'hotels':list_hotels})



def Rooms_view(request):

    list_rooms = Roomtype.objects.all()

    return render(request,'pages/rooms.html',{'rooms':list_rooms})



def Filter_room(request):
    price_filter = request.GET.get('price_filter')
    if price_filter:
        min_price, max_price = price_filter.split('-')
        list_rooms = Roomtype.objects.filter(price__gte=min_price,price__lte=max_price)

    return render(request,'pages/rooms.html',{'rooms':list_rooms})
    

# Create your views here.
