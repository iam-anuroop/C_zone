# forms.py
from django import forms
from .models import HotelDetails

class HotelRegistrationForm(forms.ModelForm):
    class Meta:
        model = HotelDetails
        exclude = ['user_id','hotel_id']    # Exclude user field as it will be set automatically


