# -*- coding: utf-8 -*-
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,)

from .models import Box


class BoxList(ListView):
    model = Box


class BoxCreate(CreateView):
    model = Box


class BoxEdit(UpdateView):
    model = Box


class BoxDetail(DetailView):
    model = Box
