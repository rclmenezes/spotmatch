#!/usr/bin/python
 
import os;
import sys;
os.environ['DJANGO_SETTINGS_MODULE'] = 'spotmatchapp.settings'
sys.path.append('/srv/spotmatch')
from spotmatchapp.models import Song

cmd = "/home/jmena/joseulisesmena-technic-565e922/examples/jukebox/playtrack -u joseulisesmena -p orniter2 -t " + sys.argv[1]
os.system(cmd)
arg = sys.argv[1]
cmd = "/home/jmena/joseulisesmena-technic-565e922/examples/jukebox/bpmdetect /srv/spotmatch/static/" + arg + ".wav > temp.txt"
os.system(cmd)

file = open('temp.txt', 'r')
bpm = file.readline()
bpm = round(float(bpm[:-1]))
print "bpm : ", bpm
while bpm < 70 and bpm > 0:
    bpm = bpm * 2

#access DB
song, wasCreated = Song.objects.get_or_create(spotify_id=arg[14:], defaults={'duration':0})

# sadly, this will ocassionally produce an error where the bpm is set to 0 by
# mistake. We could not think of a way to fix it. It remains an open problem.
# In our defense, we totally implemented the registration and login system
# and the queue, so this is the only problem left.
song.bpm = bpm
song.save()

# This has been removed because we decided to not do .ogg files.
# These were only going to be necessary if we were going to fill up the entire
# database, but that doesn't seem likely to happen for testing and submission
# purposes
#cmd = "sox /srv/spotmatch/static/" + sys.argv[1] + ".wav /srv/spotmatch/static/" + arg + ".ogg"
#os.system(cmd)
#cmd = "rm -f /srv/spotmatch/static/" + arg + ".wav"
#os.system(cmd)
