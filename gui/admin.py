from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import csv
from django.http import HttpResponse
from .models import *
admin.site.register(Account)