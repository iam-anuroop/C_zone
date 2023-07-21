from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from User_manage.models import UserDetails
import uuid




class HotelManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create a new HotelDetails instance
        hotel = self.model(email=self.normalize_email(email), **extra_fields)
        hotel.set_password(password)
        hotel.save(using=self._db)
        return hotel

# model for creating hotels 

class HotelDetails(AbstractBaseUser):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    hotel_email = models.EmailField(unique=True,null=False)
    hotel_registration_number = models.CharField(max_length=255)
    hotel_contact_number = models.CharField(max_length=20)
    hotel_address = models.CharField(max_length=255)
    hotel_location = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    hotel_profile = models.ImageField(upload_to='hotel_profile/')



    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_logined = models.BooleanField(default=False)
    is_registerd = models.BooleanField(default=False)


    USERNAME_FIELD = 'hotel_email'

    objects = HotelManager()


    def __str__(self):
        return self.hotel_name


# Hotelowner details 
class Hotelowner(models.Model):
    hotel_id = models.ForeignKey(HotelDetails,on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()
    owner_contact = models.CharField(max_length=20)
    owner_address = models.CharField(max_length=255)
    id_card = models.ImageField(upload_to='hotelowner_idcard/')



# hotel booking details of user 
class Roomtype(models.Model):
    hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    roomtype = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='room_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.roomtype



# booking details table
class BookingDetails(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.CharField(max_length=150)
    num_of_guests = models.IntegerField()
    special_requests = models.TextField()
    name = models.CharField(max_length=100)
    id_card = models.ImageField(upload_to='roomuser_idcard/')



    is_paid = models.BooleanField(default=False)
    is_advancepaid = models.BooleanField(default=False)
    


    

    def short_booking_id(self):
        return str(self.booking_id)[:8]

    def __str__(self):
        return str(self.booking_id)

