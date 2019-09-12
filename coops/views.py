from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Coop
import requests

def home(request):
    return render(request, 'coops/index.html')

def dashboard(request):
    return render(request, 'coops/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    # def form_valid(self, form):
    #     view = super(SignUp, self).form_valid(form)
    #     username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
    #     user = authenticate(username=username, password=password)
    #     login(self.request, user)
    #     return view


class login(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/login.html'


class CreateCoop(generic.CreateView):
    model = Coop 
    fields = ['title']
    template_name = 'coops/create_coop.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateCoop, self).form_valid(form)
        return redirect('dashboard')

class DetailCoop(generic.DetailView):
    model = Coop
    template_name = 'coops/detail_coop.html'

class UpdateCoop(generic.UpdateView):
    model = Coop
    template_name = 'coops/update_coop.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

class DeleteCoop(generic.DeleteView):
    model = Coop
    template_name = 'coops/delete_coop.html'
    success_url = reverse_lazy('dashboard')
