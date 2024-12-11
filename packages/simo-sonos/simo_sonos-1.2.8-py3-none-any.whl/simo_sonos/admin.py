from django.contrib import admin
from .models import SonosPlayer, SonosPlaylist


class SonosPlaylistInline(admin.TabularInline):
    extra = 0
    model = SonosPlaylist
    fields = 'id', 'title', 'item_id'
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False




@admin.register(SonosPlayer)
class SonosPlayerAdmin(admin.ModelAdmin):
    list_display = '__str__', 'ip', 'is_alive', 'last_seen', 'is_master'
    search_fields = 'name', 'ip'
    readonly_fields = 'name', 'uid', 'is_master', 'slave_of', 'is_alive', 'last_seen'
    fields = readonly_fields
    inlines = SonosPlaylistInline,

    def has_add_permission(self, request):
        return False

    def is_master(self, obj):
        return not obj.slave_of
    is_master.boolean = True


