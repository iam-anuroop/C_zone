from django.shortcuts import render,redirect,get_object_or_404
from .Hotel_form import HotelRegistrationForm  , Roomtypeform ,Bookingform,Hotelownerform
from django.contrib.auth.decorators import login_required
from User_manage.models import UserDetails
from .models import HotelDetails , Roomtype ,BookingDetails
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.


# hotel registration
@login_required(login_url='login')
def Hotelregister(request):
    if request.user == None:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = HotelRegistrationForm(request.POST,request.FILES)
            password = request.POST.get('password')
            email = request.POST.get('hotel_email')
            if form.is_valid():
                hotel = form.save(commit=False)
                user = request.user
                user.is_hoteluser = True
                hotel.user_id = request.user
                hotel.set_password(password)
                user.save()
                hotel.save()
                request.session['hotel_id']=hotel.id


                try:
                    current_site = get_current_site(request)
                    mail_subject = "Please activate your account"
                    message = render_to_string("hotel_account/email_verify.html", {
                        'user': request.user,
                        # 'hotel':hotel,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(hotel.pk)),
                        'token': default_token_generator.make_token(hotel),
                    })
                    to_email = email
                    send_mail = EmailMessage(mail_subject, message, to=[to_email])
                    send_mail.send()

                    return redirect('hotelowner_reg')
                except Exception as e:
                    messages.error(request, f"An error occurred during registration: {str(e)}")

                # logout(request) #making the user logout 
    
                return redirect('hotelowner_reg')
            else:
                messages.error(request,'invalid form')
        else:
            form= HotelRegistrationForm()
            
    return render(request,'hotel_account/hotel_reg.html',{'form': form,})


# hotel regostration second part owner details 
def ownerregistration(request):
    hotel_id = request.session.get('hotel_id')
    hotel = HotelDetails.objects.get(id=hotel_id)
    if request.method == 'POST':
        form = Hotelownerform(request.POST, request.FILES)
        if form.is_valid():
            owner=form.save(commit=False)
            hotel.is_registerd = True
            hotel.save()
            owner.hotel_id = hotel
            owner.save()
            return redirect('emailnotification')  
    else:
        form = Hotelownerform()
    return render(request,'hotel_account/hotel_owner.html',{'form':form})


#email activation for hotel account

def activatehotel(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    hotel = HotelDetails.objects.get(pk=uid)
    print(uid,hotel,token)
    try:
        if hotel is not None and default_token_generator.check_token(hotel, token):
            hotel.is_active=True
            hotel.save()
            messages.success(request, 'Account activated successfully you can now login')
            return redirect('hotellogin')
        else:
            messages.error(request, 'Invalid activation link')
    except :
        messages.error(request, 'Invalid activation link')
    return redirect('hotellogin')




# hotel login
@login_required(login_url='login')
def Hotellogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        try:
            # print('j')
            hotel = HotelDetails.objects.get(hotel_email=email)
            if check_password(password, hotel.password) and hotel.is_active==True and hotel.is_registerd ==True:  # Manually check the password
                print('Password matched!')
                hotel.is_logined = True
                hotel.save()
                request.session['hotel_id'] = hotel.id
                return redirect('hotelhome')
            else:
                # is registered
                if hotel.is_registerd == False:
                    messages.error(request,'you need to add owner details')
                    return redirect('hotelowner_reg')
                # hotelactiavte
                elif hotel.is_active == False:
                    messages.error(request,'Verify you account through the verification link')
                else:
                    messages.error(request,'Incorrect password')
                
                print('Invalid password.')
                return redirect('hotellogin')
        except HotelDetails.DoesNotExist:
            # print(hotel)

            print('User not found.')
            
    return render(request, 'hotel_account/hotel_login.html')




# hotelhome
def Hotelhome(request):
    hotel_id = request.session.get('hotel_id')

    if hotel_id:
        try:
            hotel = HotelDetails.objects.get(id=hotel_id)
            if hotel.is_logined:
                bookings = BookingDetails.objects.filter(hotel = hotel_id)
                return render(request, 'hotel_account/hotel_home.html',{'bookings':bookings})
            else:
                messages.error(request, 'You need to log in first')
                return redirect('hotellogin')
        except HotelDetails.DoesNotExist:
            messages.error(request, 'Invalid hotel details')
            return redirect('hotellogin')
    else:
        messages.error(request, 'You need to log in first')
        return redirect('hotellogin')





# logout hotel
def Hotellogout(request):
    hotel_id = request.session.get('hotel_id')
    if hotel_id is not None:
        hotel = get_object_or_404(HotelDetails, id=hotel_id)
        hotel.is_logined = False
        hotel.save()
    else:
        pass    
    # Always redirect to the hotel login page after logout.
    return redirect('hotellogin')

# room type 
def Roomtype_view(request):
    hotel_id = request.session.get('hotel_id')
    if hotel_id is None:
        messages.error(request, 'You need to login first')
        return redirect('hotellogin')

    try:
        hotel = HotelDetails.objects.get(id=hotel_id, is_logined=True)
    except HotelDetails.DoesNotExist:
        messages.error(request, 'You need to login first')
        return redirect('hotellogin')

    if request.method == 'POST':
        form = Roomtypeform(request.POST, request.FILES)

        if form.is_valid():
            room = form.save(commit=False)
            room.hotel_id = hotel
            room.save()
            messages.success(request, 'Room type added successfully.')
            return redirect('roomtypeupdate')
        else:
            messages.error(request, 'Form is not valid. Please check the data you entered.')
    else:
        form = Roomtypeform()

    datas = Roomtype.objects.filter(hotel_id=hotel_id)
    return render(request, 'hotel_account/roomtype.html', {'datas': datas, 'form': form})





def hotel_book(request,hotel_id):
    hotel = get_object_or_404(HotelDetails, id=hotel_id)
    rooms = Roomtype.objects.filter(hotel_id=hotel_id)
    if request.method == 'POST':
        form =Bookingform(request.POST,request.FILES)

        # Save the booking data to the database
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel = hotel
            booking.user = request.user  # Assuming the user is authenticated
            booking.save()

        # booking.save()

    # form = Bookingform()
    return render(request,'pages/hotelbook.html',{'hotel':hotel,'rooms':rooms})

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