from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Coop, Video
from .forms import VideoForm, SearchForm
import requests
from django.http import Http404
import urllib 
from django.forms.utils import ErrorList

YOUTUBE_API_KEY = 


def home(request):
    return render(request, 'coops/index.html')

def dashboard(request):
    return render(request, 'coops/dashboard.html')

def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    coop = Coop.objects.get(pk=pk)
    if not coop.user == request.user:
        raise Http404

    if request.method == 'POST':

        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.coop = coop
            video.url = filled_form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_coop', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a YouTube URL')

    return render(request, 'coops/add_video.html', {'form': form, 'search_form': search_form, 'coop': coop })

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
