from spotmatchapp.models import *
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    list_display = ('spotify_id', 'name', 'artist', 'album')
    search_fields = ['spotify_id', 'name', 'artist', 'album', 'duration']
    
class SongRequestAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['user__username', 'song__name', 'song__artist']
    
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ['name', 'user__username']
    
admin.site.register(Song, SongAdmin)
admin.site.register(SongRequest, SongRequestAdmin)
admin.site.register(Playlist, PlaylistAdmin)