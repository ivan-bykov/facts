from django.conf.urls import patterns, url
from facts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^days/$', views.days, name='days'),
    url(r'^days/rest/$', views.rest, name='rest'),
    url(r'^(?P<fact_id>\d+)/(?P<field>\S+)/$', views.data, name='data'),
    )
