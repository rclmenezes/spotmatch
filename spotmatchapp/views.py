import os, sys
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_detail
from spotmatchapp.models import *
#from path3 import find_path
from django.utils import simplejson
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from forms import RegisterForm
from search import get_query
from hashlib import md5

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()

    return render_to_response("register.html", {'form':form, })
    
def activate_user(username,  code):
    if code == md5(username).hexdigest():
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return True
    else:
        return False
        
def activate(request):
    user = request.GET.get('user')
    code = request.GET.get('code')

    if activate_user(user,  code):
        return HttpResponseRedirect("/activated")
    else:
        raise Http404

def check_file_size(spotify_id):
    file_path = "/srv/spotmatch/static/spotify:track:" + spotify_id + ".wav"
    try:
        statinfo =  os.stat(file_path)
        return statinfo.st_size
    except:
        return 0

def home(request):
    if not request.user.is_authenticated():
        return render_to_response('home.html', {'user': request.user})
    else:
        return HttpResponseRedirect("/your_playlists")
    
def create_playlist(request):
    if request.method == 'POST' and 'songs' in request.POST and 'playlist-name' in request.POST:
        name = request.POST['playlist-name']
        songs = simplejson.loads(request.POST['songs'])
        playlist, created = Playlist.objects.get_or_create(user=request.user, name=name)
        
        playlist_songs = PlaylistSong.objects.filter(playlist=playlist)
        for song in playlist_songs:
            song.delete()
        
        for index, song in enumerate(songs):
            track_id = song['track_id'][14:] # Removes first part
            name = song['name']
            artist = song['artist']
            album = song['album']
            duration = song['duration']
            song, created = Song.objects.get_or_create(spotify_id=track_id, name=name, artist=artist, album=album, duration=duration)
            playlist_song = PlaylistSong(playlist=playlist, song=song, order=index)
            playlist_song.save()
            
            if created or song.bpm is None:
                song_request = SongRequest(user=request.user, song=song)
                song_request.save()
        
        return HttpResponseRedirect("/playlist/" + str(playlist.pk))

    return render_to_response('create_playlist.html', {'user': request.user})
    
def your_playlists(request):
    top_playlists = Playlist.objects.order_by('-upvotes')[:10]
    your_playlists = Playlist.objects.filter(user=request.user).order_by('-upvotes')
    return render_to_response('your_playlists.html', {'user': request.user, 'top_playlists': top_playlists, 'your_playlists': your_playlists})
    
def playlists(request):
    return render_to_response('playlists.html')
    
def playlist(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk)
    playlist_songs = PlaylistSong.objects.filter(playlist=playlist).order_by('order')
    
    if request.user.is_authenticated():
        user = request.user
        upvote = PlaylistUpvote.objects.filter(user=user, playlist=playlist).exists()
        owner = (playlist.user == user)
    elif int(playlist_pk) == 6:
        upvote = False
        owner = False
        user = None
    else:
        raise Http404
    
    ready = True
    for playlist_song in playlist_songs:
        ready = ready and playlist_song.song.file_present()
    
    return render_to_response('playlist.html', {'user': user, 'playlist': playlist, 'upvote': upvote, 'playlist_songs': playlist_songs, 'owner': owner, 'ready': ready})

def beatmatch(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk)
    playlist_songs = PlaylistSong.objects.filter(playlist=playlist).order_by('order')
    
    f = open("/srv/spotmatch/static/" + str(playlist_pk) + '.txt', 'w')
    
    f.write(str(playlist_pk) + '\n')
    for playlist_song in playlist_songs:
        f.write(str(playlist_song.song.spotify_id) + '\n')
        
    f.close()
    
    command = 'python /srv/spotmatch/beatmatch.py /srv/spotmatch/static/'+ str(playlist_pk) + '.txt > /srv/spotmatch/static/' + str(playlist_pk) + "_out.txt"
    a = os.system(command)
    return HttpResponse(command + " " + str(a))
    
def upvote(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk)
    upvote_exists = PlaylistUpvote.objects.filter(user=request.user, playlist=playlist).exists()
    if upvote_exists:
        upvote = PlaylistUpvote.objects.get(user=request.user, playlist=playlist)
        upvote.delete()
        playlist.upvotes -= 1
        playlist.save()
    else:
        upvote = PlaylistUpvote(user=request.user, playlist=playlist)
        upvote.save()
        playlist.upvotes += 1
        playlist.save()

    return HttpResponse("Success")
    
def edit(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    playlist_songs = PlaylistSong.objects.filter(playlist=playlist).order_by('order')

    return render_to_response('create_playlist.html', {'user': request.user, 'playlist': playlist, 'playlist_songs': playlist_songs})
    
def delete(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    return render_to_response('delete.html', {'playlist': playlist})
       
def deleted(request, playlist_pk):
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    playlist.delete()
    return render_to_response('deleted.html')
    
def activated(request):
    return render_to_response('activated.html')
    
def activate_soon(request):
    return render_to_response('activate_soon.html')
    
def search(request):
    if 'search' in request.GET:
        query = request.GET['search']
        if query != "" and query.strip() != "": 
            playlist_list = Playlist.objects.filter(get_query(query, ['name'])).order_by('-upvotes')
    return render_to_response('search.html', {'playlist_list': playlist_list})
    
def logout(request):
    logout(request)
    return HttpResponseRedirect("/")
    
def makePlaylist(request):
    if request.method == 'POST' and 'track_id' in request.POST and 'artist' in request.POST and 'album' in request.POST and 'name' in request.POST and 'duration' in request.POST and len(request.POST['track_id']) <= 36:
        track_id = request.POST['track_id'][14:] # Removes first part
        name = request.POST['name']
        artist = request.POST['artist']
        album = request.POST['album']
        duration = request.POST['duration']
        # Make sure lengths are compatible with db
        if len(name) > 200:
            name = name[:200]
        if len(artist) > 200:
            artist = artist[:200]
        if len(album) > 200:
            album = album[:200]
        song, created = Song.objects.get_or_create(spotify_id=track_id, name=name, artist=artist, album=album, duration=duration)
        
        size = check_file_size(track_id)
        if size < 4000000:
            cmd = "/home/jmena/joseulisesmena-technic-565e922/examples/jukebox/playtrack -u joseulisesmena -p orniter2 -t spotify:track:" + track_id
            os.system(cmd)
            return HttpResponse("Getting file")
        return HttpResponse("Already have")
    raise Http404
