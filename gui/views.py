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
# global web_cam
# Create your views here.
# while True:
#     print(context)

message = ""
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
    global web_cam, message
    web_cam = Webcam()
    return StreamingHttpResponse(web_cam.read(),
                    content_type='multipart/x-mixed-replace; boundary=frame')
    # return render(request, 'camera.html', {'img':web_cam.read()})

def webcam_home(request):   
    return render(request, 'camera.html', context={})
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

def acc_settings_view(request):
    context = {}
    if request.user.is_authenticated:
        user = Account.objects.get(email=request.user.email)
        edit_form = SettingsForm(request.POST or None, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('logout')
        context['form'] = edit_form
        return render(request, 'acc_settings.html', context)
    else:
        return redirect('login')

def setting_view(request):
    context = {}
    if request.user.is_authenticated:
        user = Account.objects.get(email=request.user.email)
        form = ChangeAlertForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('logout')
        context['form'] = form
        return render(request, 'settings.html', context)
    else:
        return redirect('login')
def logout_view(request):
    global web_cam
    web_cam.stop()
    cv2.destroyAllWindows()
    logout(request)
    return redirect('login')