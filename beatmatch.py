#!/usr/bin/python
import os
import sys
from cluster import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'spotmatchapp.settings'
sys.path.append('/srv/spotmatch');
import collections
from spotmatchapp.models import Song

import copy
import math
id = [];
bpm = [];
song2bpm = {};
f = open(sys.argv[1],'r');
play = f.readline()
play = play[0:-1]
f3 = open('/srv/spotmatch/static/' + play + '_clust.txt', 'r');

f2 = open('/srv/spotmatch/static/' + play + '_clust.txt', 'w');
for line in f:
    id.append(line.rstrip("\n"))

for line in f3:
    if (is_number(line)):
        print
    else:
        if id.contains(line):
            print
        else:
            exit

    
data = collections.defaultdict(list)
for i in id:
    print i
    song = Song.objects.get(spotify_id=i)
    while song.bpm < 70 and song.bpm > 0:
        song.bpm = song.bpm * 2
    bpm.append(song.bpm)
    song2bpm[i] = song.bpm
    data[song.bpm].append({'bpm':song.bpm, 'id':i})

cl = HierarchicalClustering(bpm,lambda x,y: float(abs(x-y)))
a = cl.getlevel(8)
cent = collections.defaultdict(list);
centbpm = [];
for s in a:
    meanbpm = mean(s)
    centbpm.append(meanbpm)
    for k in s:
        for l in data[k]:
            if l['id'] in cent[meanbpm]:
                print 
            else:
                cent[meanbpm].append(l['id'])
                #print cent[meanbpm]


pref = 'spotify:track:'
for mbpm in centbpm:
    f2.write(str(mbpm) + "\n")
    for song in cent[mbpm]:
        if song2bpm[song] == 0:
            cmd = "cp /srv/spotmatch/static/" + pref + song + ".wav /srv/spotmatch/static/" + pref + song + '_' + play + '.wav'
            os.system(cmd)
        else:
            delbpm = (mbpm -song2bpm[song] )/song2bpm[song] * 100
            cmd = '/srv/spotmatch/beatstretch /srv/spotmatch/static/' + pref + song + '.wav /srv/spotmatch/static/' + pref + song + '_' + play + '.wav ' + str(delbpm)
            print cmd
            os.system(cmd)
        
        f2.write(song + "\n");            
        cmd = "sox /srv/spotmatch/static/" + pref + song + '_' + play + ".wav /srv/spotmatch/static/" + pref + song + '_' + play + ".ogg"
        os.system(cmd)
        cmd = "rm -f /srv/spotmatch/static/" + pref + song + '_' + play + ".wav"
        os.system(cmd)
        


#stack overflow

def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
