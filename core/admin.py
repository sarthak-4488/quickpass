from django.contrib import admin
from .models import student,Town,buspass,Clerk
# Register your models here.
admin.site.register(student)
admin.site.register(Town)
admin.site.register(buspass)
admin.site.register(Clerk)