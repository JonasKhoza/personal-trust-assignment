from django import forms
from django.forms import inlineformset_factory

from .models import Address, Client


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["client"]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'id_number']

AddressFormSet = inlineformset_factory(Client, Address, form=AddressForm, extra=2, can_delete=False)