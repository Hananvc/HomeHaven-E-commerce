from .models import Coupon
from django import forms


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'min_value', 'valid_from', 'valid_at', 'active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'First Name', 'class':'form-control','style':'max-width:300px; margin-left:115px'}),
            'valid_at': forms.DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'First Name','class':'form-control', 'style':'max-width:300px; margin-left:115px'}),
            'code': forms.TextInput(attrs={'placeholder': 'Coupon code', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
            'discount': forms.TextInput(attrs={'placeholder': 'Discount', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
            'min_value': forms.TextInput(attrs={'placeholder': 'Minimum value', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),



        }