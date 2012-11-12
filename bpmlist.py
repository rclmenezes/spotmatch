import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'spotmatchapp.settings'
sys.path.append('/srv/spotmatch')

from spotmatchapp.models import Song

#reads in songlist.txt file
songlist = open('static/songlist.txt',mode='r').readlines()

for song in songlist:
    #run beat detection
    cmd = '/home/jmena/joseulisesmena-technic-565e922/examples/jukebox/bpmdetect ' + '/srv/spotmatch/static/' + song
    bpm = os.popen(cmd).readline()
    
    #add to DB
    songid = song[14:-5]

    song, wasCreated = Song.objects.get_or_create(spotify_id=songid, defaults={'duration':0})
    song.bpm = round(float(bpm))
    song.save()

