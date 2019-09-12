from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Coop

def home(request):
    return render(request, 'coops/index.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class login(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'

class CreateCoop(generic.CreateView):
    model = Coop 
    fields = ['title']
    template_name = 'coops/create_coop.html'
    success_url = reverse_lazy('home')