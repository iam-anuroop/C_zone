from django.db import models
from User_manage.models import UserDetails
import uuid

class HotelDetails(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    hotel_id = models.CharField(primary_key=True, max_length=8, editable=False)
    hotel_name = models.CharField(max_length=255)
    hotel_email = models.EmailField()
    hotel_registration_number = models.CharField(max_length=255)
    hotel_contact_number = models.CharField(max_length=20)
    hotel_address = models.CharField(max_length=255)
    hotel_location = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    hotel_profile = models.ImageField(upload_to='hotel_profile/')
    hotel_owner_name = models.CharField(max_length=255)
    hotel_owner_email = models.EmailField()
    hotel_owner_contact = models.CharField(max_length=20)
    hotel_owner_address = models.CharField(max_length=255)


    def save(self, *args, **kwargs):
        if not self.hotel_id:
            self.hotel_id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hotel_name
