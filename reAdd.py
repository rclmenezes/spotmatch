#!/usr/bin/python

# This takes the songs we couldn't get from requests and reAdds them
# in the hopes that we can dowload them later
# This is also called via a cronjob

import os;
import sys;
os.environ['DJANGO_SETTINGS_MODULE'] = 'spotmatchapp.settings'
sys.path.append('/srv/spotmatch')
from spotmatchapp.models import *

import copy

def reAddSongs():
    # Get songs we didn't get
    requests = Song.objects.filter(bpm=-1);
        
    # Re-Add to requests

    for r in requests:
        SongRequest.add(r) 
        r.delete();

        song = Song.objects.get(spotify_id = request.song.spotify_id)
        song.bpm = -1;
        song.save();

    request.delete();
        
reAddSongs();
