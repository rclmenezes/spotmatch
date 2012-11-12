#!/usr/bin/python

# Since songs can take quite a while to download, and since we can only 
# download one at a time, we need a system to download one song at a time,
# analyze it, and add it to the database.
# This is our implementation for the queue that fetches requested songs.
# It works, but there are some issues with how tracks themselves act
# that we had to address.
# This is called every 5 minutes via a cron job.

import os;
import sys;
os.environ['DJANGO_SETTINGS_MODULE'] = 'spotmatchapp.settings'
sys.path.append('/srv/spotmatch')
from spotmatchapp.models import *

import copy
import subprocess;
import threading

# A debug flag. True signs that this project deserves an A+ for design
DEBUG = 0;

# This lets us thread commands. Highly useful in order to implement our timeout
# for songs that won't download for whatever reason.
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            # print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            # print 'Thread finished'
            return 'success'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            # print 'Terminating process'
            self.process.terminate()
            thread.join()
            return 'failed'
        return self.process.returncode

def fetchSongs():
    # Get first song
    request = SongRequest.objects.order_by('added')[0];
        
    if DEBUG == 1:
        print request.added;

    # Download

    # Let's try to download this song several times. If this succeeds 
    # at any point, break out of the loop and just delete the song from
    # the requests table. If it doesn't succeed after the set number of
    # tries (checks, rather), set the bpm of the song to -1, used as
    # a flag value.
    cmd = "python maketrack.py spotify:track:" + request.song.spotify_id
    if DEBUG == 1:
        print cmd;
    command = Command(cmd)

    timeout = 20;
    tries = 0;
    while tries < 10:
        tries += 1;
        output = command.run(timeout)
        if output == 'success':
            break;

    # Sometimes, the song download just won't start.
    # We tried to deal with this as follows, but the solution is not perfect.
    # Sometimes, this is just an error with the track itself being bad.
    # We deal with this by blacklisting said track.
    if output == 'failed':
        if DEBUG == 1:
            print 'Well, shit'
        # Here, the song didn't download. We will blacklist it with the -1 bpm flag
        song = Song.objects.get(spotify_id = request.song.spotify_id)
        song.bpm = -1;
        song.save();

    request.delete();
        
    # Beatmatchings currently requires .wav files so we have turned
    # conversion to .ogg off.
    # cmd = "sox /srv/spotmatch/static/" + request.song + ".wav /srv/spotmatch/static/" + arg + ".ogg"
    #if DEBUG == 1:
    #    print "requested id: ", cmd
    #os.system(cmd)
    
    # Similarly, given that we never convert to .ogg, removing the original .wav
    # file is the worst idea we can have.
    #cmd = "rm /srv/spotmatch/static/" + request.song + ".wav"
    #os.system(cmd)

fetchSongs();
