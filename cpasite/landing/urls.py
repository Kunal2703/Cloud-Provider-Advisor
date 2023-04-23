from django.contrib import admin
from django.urls import path
from landing import views

urlpatterns = [
    path("", views.land, name='land'),
    path("login", views.login, name='login'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("home", views.home, name='home'),
    path("index", views.index, name='index')
]