from django.urls import path
from django.contrib.auth import views as auth_views

from client.views import ClientDetailView, ClientList, HomeView, ClientCreateView
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("clients/", ClientList.as_view(), name="client_list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clients/new", ClientCreateView.as_view(), name='client_create'),
]
 