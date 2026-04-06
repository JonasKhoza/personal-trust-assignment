from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from .models import Address, Client, Relationship


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["client"]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'id_number']

AddressFormSet = inlineformset_factory(Client, Address, form=AddressForm, extra=2, can_delete=False)

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ["client_to", "relationship_type"]

    def __init__(self, *args, **kwargs):
        self.client_from = kwargs.pop("client_from")
        super().__init__(*args, **kwargs)
        # Exclude the current client from the dropdown
        self.fields["client_to"].queryset = Client.objects.exclude(id=self.client_from.id)

    def clean(self):
        cleaned_data = super().clean()
        client_to = cleaned_data.get("client_to")

        if not client_to:
            return cleaned_data

        # self relationship
        if client_to == self.client_from:
            raise ValidationError("A client cannot have a relationship with themselves.")


        if Relationship.objects.filter(
                client_from=self.client_from,
                client_to=client_to
            ).exists() or Relationship.objects.filter(
                client_from=client_to,
                client_to=self.client_from
            ).exists():
                raise ValidationError("Relationship already exists between these clients.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.client_from = self.client_from  

        if commit:
            instance.save()

        return instance

    