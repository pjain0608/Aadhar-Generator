from django.contrib import admin
from .models import Aadhar


@admin.register(Aadhar)
class AdminStudent(admin.ModelAdmin):
    list_display = ['id','first_name','aadhar']
    list_display_links = ['first_name']

