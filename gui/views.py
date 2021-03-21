from django.shortcuts import render, redirect
from gui.templates import *
from django.http import StreamingHttpResponse
from django.contrib.auth import login, authenticate, logout
from django.template import Context, Template
import cv2
import threading
import gzip
from .camera import Webcam
from .models import *
from .forms import *

# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'login.html', context=context )

def gen(webcam):
    while True:
        frame = webcam.get_frame()     
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')
def webcam_feed(request):
    web_cam = Webcam()
    return StreamingHttpResponse(web_cam.read(),
                    content_type='multipart/x-mixed-replace; boundary=frame')
    # return render(request, 'camera.html', {'img':web_cam.read()})

def webcam_home(request):
    return render(request, 'camera.html')
def registration_view(request):
    context = {}
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            account = registration_form.save()
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = registration_form
    else:
        registration_form = RegistrationForm()
        context['registration_form'] = registration_form
    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = MyAccountManager.normalize_email(form.cleaned_data['email'])
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'login_form':form})

def logout_view(request):
    logout(request)
    return redirect('login')