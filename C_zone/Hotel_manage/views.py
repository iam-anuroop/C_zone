from django.shortcuts import render,redirect
from .Hotel_form import HotelRegistrationForm 
from django.contrib.auth.decorators import login_required
from User_manage.models import UserDetails
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.


@login_required(login_url='login')
def Hotelregister(request):
    # user_pk = request.session.get('pk')
    form= HotelRegistrationForm()
    # if not request.user.is_authenticated:
    #     return redirect('login')
    if request.user =='' or request.user == None:
        return redirect('login')
    else:
        # user = UserDetails.objects.get(pk=user_pk)
        if request.method == 'POST':
            form = HotelRegistrationForm(request.POST,request.FILES)
            if form.is_valid():
                hotel = form.save(commit=False)
                hotel.user_id = request.user
                hotel.save()
                logout(request)
                return redirect('registration')
            else:
                messages.error(request,'invalid form')
    
    return render(request,'hotel_account/hotel_reg.html',{'form': form,})




    # hotel_name = form.cleaned_data['hotel_name']
    # hotel_email = form.cleaned_data['hotel_email']
    # hotel_registration_number = form.cleaned_data['hotel_registration_number']
    # hotel_contact_number = form.cleaned_data['hotel_contact_number']
    # hotel_address = form.cleaned_data['hotel_address']
    # hotel_location = form.cleaned_data['hotel_location']
    # district = form.cleaned_data['district']
    # state = form.cleaned_data['state']
    # city = form.cleaned_data['city']
    # pin_code = form.cleaned_data['pin_code']
    # hotel_owner_name = form.cleaned_data['hotel_owner_name']
    # hotel_owner_email = form.cleaned_data['hotel_owner_email']
    # hotel_owner_contact = form.cleaned_data['hotel_owner_contact']
    # hotel_owner_address = form.cleaned_data['hotel_owner_address']
    # return
