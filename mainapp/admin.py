from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Topplaces)
admin.site.register(Tophotels)

