from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.exceptions import ValidationError

from client.models import Address, Client
from .forms import ClientForm, AddressFormSet, RelationshipForm

class HomeView(TemplateView):
    template_name = "home.html"


class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        if request.headers.get("HX-Request"):
            return render(request, "partials/client_table.html", {
                "object_list": self.object_list
            })

        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(id_number__icontains=query)
            )

        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.object

        # Relationships
        context["relationships"] = client.relationships_from.select_related("client_to")

        # Addresses
        addresses = client.address_set.all()

        context["physical_address"] = addresses.filter(address_type=0).first()
        context["postal_address"] = addresses.filter(address_type=1).first()

        return context


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
                #first I should add: ensure the two addresses are not of the same type, have the right fields filled

                address.client = client
                address.save()
            return redirect('client_list')

        return render(request, self.template_name, {
            'client_form': client_form,
            'address_formset': address_formset
        })


class RelationshipCreateView(LoginRequiredMixin, View):
    template_name = "add_relationship.html"

    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = RelationshipForm(client_from=client)
        return render(request, self.template_name, {"form": form, "client": client})
    
    def post(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = RelationshipForm(request.POST, client_from=client)

        if form.is_valid():
            try:
                form.save()
                return redirect("client_detail", pk=client.id)
            except ValidationError as e:
                form.add_error(None, e)

        return render(request, self.template_name, {"form": form, "client": client})