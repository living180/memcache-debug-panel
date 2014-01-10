from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'demo.views.index', {}, 'index'),
    url(r'^cached$', 'demo.views.cached', {}, 'cached'),
)
