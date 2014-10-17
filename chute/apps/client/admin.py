# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner')
    search_fields = ('name', 'slug', 'owner__first_name', 'owner__last_name')

    def get_queryset(self, request):
        return super(ClientAdmin, self).queryset(request=request).select_related('lawyer')


admin.site.register(Client, ClientAdmin)


