from django.conf.urls.defaults import *

from adzone.views import ad_view, ad_display

urlpatterns = patterns('',
    url(r'^view/(?P<id>[\d]+)/$', ad_view, name='adzone_ad_view'),
    url(r'^addisplay.html', ad_display, name='adzone_ad_display'),
)
