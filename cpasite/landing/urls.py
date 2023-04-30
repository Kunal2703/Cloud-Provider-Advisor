from django.contrib import admin
from django.urls import path
from landing import views

urlpatterns = [
    path("", views.land, name='land'),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name='signout'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("index", views.index, name='index')
]