from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Coop, Video
from .forms import VideoForm, SearchForm
import requests
from django.http import Http404, JsonResponse
import urllib 
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

YOUTUBE_API_KEY = 'AIzaSyDgz0oNhLXGcDSD5zPN5QxGK0Ho4OUeVLY'

def home(request):
    recent_coops = Coop.objects.all().order_by('-id')[:3]
    popular_coops = [Coop.objects.get(pk=1), Coop.objects.get(pk=2), Coop.objects.get(pk=3)]
    return render(request, 'coops/index.html', {'recent_coops': recent_coops, 'popular_coops': popular_coops})

@login_required
def dashboard(request):
    coops = Coop.objects.filter(user=request.user)
    return render(request, 'coops/dashboard.html', {'coops':coops})

@login_required
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

@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'coops/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.coop.user == self.request.user:
            raise Http404
        return video


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
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


class CreateCoop(LoginRequiredMixin, generic.CreateView):
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

class UpdateCoop(LoginRequiredMixin, generic.UpdateView):
    model = Coop
    template_name = 'coops/update_coop.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        coop = super(UpdateCoop, self).get_object()
        if not coop.user == self.request.user:
            raise Http404
        return coop

class DeleteCoop(LoginRequiredMixin, generic.DeleteView):
    model = Coop
    template_name = 'coops/delete_coop.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        coop = super(DeleteCoop, self).get_object()
        if not coop.user == self.request.user:
            raise Http404
        return coop