from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^/?$', 'spotmatchapp.views.home', name='home'),
    url(r'^beatmatch/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.beatmatch'),
    url(r'^playlists/?$', 'spotmatchapp.views.playlists'),
    url(r'^playlist/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.playlist'),
    url(r'^upvote/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.upvote'),
    url(r'^delete/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.delete'),
    url(r'^deleted/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.deleted'),
    url(r'^edit/(?P<playlist_pk>\d+)/?$', 'spotmatchapp.views.edit'),
    url(r'^search/?$', 'spotmatchapp.views.search'),
    url(r'^activated/?$', 'spotmatchapp.views.activated'),
    url(r'^activate_soon/?$', 'spotmatchapp.views.activate_soon'),
    url(r'^makePlaylist/?$', 'spotmatchapp.views.makePlaylist'),
    url(r'^create_playlist/?$', 'spotmatchapp.views.create_playlist'),
    url(r'^your_playlists/?$', 'spotmatchapp.views.your_playlists'),

    #authentication
    url(r'register/?$','spotmatchapp.views.register', name="register"),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout , {'next_page': '/'}, name="logout"),
    url(r'activate/$',  'spotmatchapp.views.activate',  name="activate"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
