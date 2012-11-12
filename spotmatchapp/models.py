from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    spotify_id = models.CharField(primary_key=True, max_length=22)
    bpm = models.IntegerField(blank=True, null=True)
    duration = models.FloatField()
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    
    def file_present(self):
        if not self.bpm:
            return False
        return True
        
    def __unicode__(self):
        return self.name
    
class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name="SpotmatchUser")
    upvotes = models.IntegerField(default=0)
    
    def get_upvotes(self):
        upvotes = PlaylistUpvote.objects.filter(playlist=self)
        return len(upvotes)
        
class PlaylistSong(models.Model):
    playlist = models.ForeignKey('Playlist', related_name="song-playlist")
    song = models.ForeignKey('Song', related_name="playlist-song")
    order = models.IntegerField()
    
class PlaylistUpvote(models.Model):
    playlist = models.ForeignKey('Playlist', related_name="PlaylistUpvote")
    user = models.ForeignKey(User, related_name="UserUpvote")
    
class SongRequest(models.Model):
    user = models.ForeignKey(User, related_name="Requester")
    song = models.ForeignKey('Song', related_name="song")
    added = models.DateTimeField(auto_now_add=True)