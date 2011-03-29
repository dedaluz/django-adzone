from django.conf.urls.defaults import *

from adzone.views import ad_view, ad_display, ad_index, xhr_ad_table

urlpatterns = patterns('',
    url(r'^view/(?P<id>[\d]+)/$', ad_view, name='adzone_ad_view'),
    url(r'^addisplay.html', ad_display, name='adzone_ad_display'),
    url(r'^ads/$', ad_index, name='adzone_ad_index'),
    #url(r'^ads/<?P<id>[\d]+)/$', ad_detail, name='adzone_ad_detail'),
    url(r'^xhr_ads/(?P<format>\w+)$', xhr_ad_table, name='adzone_xhr_ad_table'),
)
