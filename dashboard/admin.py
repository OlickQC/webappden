from django.contrib import admin

# Register your models here.

from .models import Inventaire, Notes

# Register your models here.

admin.site.register(Inventaire)
admin.site.register(Notes)