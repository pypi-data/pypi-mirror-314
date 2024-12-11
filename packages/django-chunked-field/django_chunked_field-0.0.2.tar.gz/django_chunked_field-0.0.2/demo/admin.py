from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MyModel


class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'json_data')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(MyModel, MyModelAdmin)
