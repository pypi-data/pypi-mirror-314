from django.contrib import admin

from .models import DataChunk


@admin.register(DataChunk)
class DataChunkAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'field_name', 'sequence')
    list_filter = ('content_type', 'field_name')
    search_fields = ('content',)
