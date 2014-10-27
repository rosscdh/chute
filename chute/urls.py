from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin

from chute.apps.project.views import FacebookWebhookView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include('chute.api.urls')),

    url(r'^me/password/', include('password_reset.urls')),
    url(r'^me/', include('chute.apps.me.urls', namespace='me')),

    url(r'^project/', include('chute.apps.project.urls', namespace='project')),

    url(r'^webhook/facebook/(?P<project_slug>[\d\w-]+)/', FacebookWebhookView.as_view()),

    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    #url(r'^', TemplateView.as_view(template_name='base.html'), name='base'),
    url(r'^', include('chute.apps.public.urls', namespace='public')),
)


if settings.DEBUG is True:
    # Add the MEDIA_URL to the dev environment
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)