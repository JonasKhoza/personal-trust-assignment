from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from client.models import Address, Client
from .forms import ClientForm, AddressFormSet

class HomeView(TemplateView):
    template_name = "home.html"


class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_details.html"

class ClientCreateView(LoginRequiredMixin, View):
    template_name = "client_create.html"
    def get(self, request):
        client_form = ClientForm()
        address_formset = AddressFormSet()
        return render(request, self.template_name, { 'client_form': client_form,'address_formset': address_formset})
    
    def post(self, request):
        client_form = ClientForm(request.POST)
        address_formset = AddressFormSet(request.POST)

        if client_form.is_valid() and address_formset.is_valid():
            
            client = client_form.save()
            addresses = address_formset.save(commit=False)
            for address in addresses:
                #first: ensure the two addresses are not of the same type, have the right fields filled


                address.client = client
                address.save()
            return redirect('client_list')

        return render(request, self.template_name, {
            'client_form': client_form,
            'address_formset': address_formset
        })
