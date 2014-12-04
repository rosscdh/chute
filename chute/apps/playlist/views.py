# -*- coding: utf-8 -*-
from django.views.generic import (DetailView,)
from .models import (Playlist,)


# Create your views here.
class PlaylistBoxesView(DetailView):
    template_name = 'playlist/playlist_boxes.html'
    model = Playlist
