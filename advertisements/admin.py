from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'creator', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_editable = ('status', 'creator')
    ordering = ['creator', '-status']
    fields = ['title', 'description', 'status', 'creator']
    save_on_top = True
    list_per_page = 10
