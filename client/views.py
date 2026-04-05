from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from client.models import Address, Client


class HomeView(TemplateView):
    template_name = "home.html"


class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_details.html"
