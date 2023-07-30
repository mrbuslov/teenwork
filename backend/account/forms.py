from django.forms import ModelForm
from account.models import Account
from django import forms

class ProfileEditForm(ModelForm):
    class Meta:
        model = Account
        fields=('image', 'first_name', 'last_name', 'person_age', 'phone_number', 'im_working_student')    