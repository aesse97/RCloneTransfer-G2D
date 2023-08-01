from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import TransferJob
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import UserLoginForm
from django.conf import settings
import requests
from django.views import View
from django.utils.decorators import method_decorator

class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        jobs = TransferJob.objects.filter(user=user).order_by('-time_started')
        return render(request, 'home.html', {'jobs': jobs})

class LoginView(View):
    def post(self, request):
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')

    def get(self, request):
        login_form = UserLoginForm()
        return render(request, 'login.html', {'login_form': login_form})

class RegisterUserView(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

class GoogleFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'googleform.html')

class DropboxFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'dropboxform.html')

class ChooseFoldersView(View):
    def get(self, request):
        return render(request, template_name='choosefolders.html')

class RCloneButtonView(View):
    def get(self, request):
        return render(request, 'rclonebutton.html')

class RCloneJobView(View):
    @method_decorator(login_required)
    def post(self, request):
        username = request.user.username
        source = request.POST.get('source')
        destination = request.POST.get('destination')

        try:
            self.trigger_jenkins_job(username, source, destination)
            message = 'Job started successfully'
        except Exception as e:
            message = f'Failed to start job: {str(e)}'

        return render(request, 'rclone_job.html', {'message': message})

    @staticmethod
    def trigger_jenkins_job(username, source, destination):
        url = f'http://localhost:8080/job/RCloneTransfer/buildWithParameters'
        params = {
            'token': settings.JENKINS_API_TOKEN,
            'username': username,
            'source': 'gdrive:',
            'destination': 'dropbox:'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()