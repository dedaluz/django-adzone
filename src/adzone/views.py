#! /usr/bin/env python
# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from datetime import datetime 
from django.db.models import Q
import operator
from django.shortcuts import render_to_response 
from django.shortcuts import get_object_or_404 
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from django.template import RequestContext 
from django.contrib.auth.decorators import permission_required 
from django.core import serializers 
from adzone.models import AdBase, AdClick, BannerAd, TextAd 

def ad_view(request, id):
    """
    Record the click in the database, then redirect to ad url

    """
    ad = get_object_or_404(AdBase, id=id)
    try:
        if not request.excluded_ip:
        	click = AdClick(ad=ad, click_date=datetime.now(), source_ip=request.META.get('REMOTE_ADDR'))
        	click.save()
    except:
        raise Http404
    return HttpResponseRedirect(ad.url)



def ad_display(request):
    """
    Simply pull an ad from the db and display it as a raw img.
    This was added to interface with legacy apps in iframes.
    Currently it's hardwired to calendar zone, but could be made scriptabled via GET params.
    """
    context = RequestContext(request)
    ad = AdBase.objects.get_random_ad('', 'calendar')
    if (context.has_key('from_ip') and ad) and not request.excluded_ip:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(ad=ad, impression_date=datetime.now(), source_ip=from_ip)
            impression.save()
        except:
            pass
    return render_to_response('adzone/ad_display.html', locals(), context_instance=RequestContext(request))


@permission_required('adzone.change_adbase')
def ad_index(request):
    ad_list=[]
    if request.GET:
        q = request.GET.get('q')
        qs=[Q()]
        try:
            qs.append(Q(impression_date__gte=q.items()[0]))
        except:
            pass
        try:
            qs.append(Q(impression_date__lte=q.items()[1]))
        except:
            pass
        ads = AdBase.objects.enabled()  
        if (q is not None):
            for ad in ads:
                ad_list.append([ad, ad.adimpression_set.filter(reduce(operator.and_, qs)).count(),
                                     ad.adclick_set.filter(reduce(operator.and_, qs)).count()])
    else:
        ads = AdBase.objects.enabled()  
        for ad in ads:
            ad_list.append([ad, ad.adimpression_set.all().count(),
                                ad.adclick_set.all().count()])
    return render_to_response('adzone/ad_index.html', locals(), context_instance=RequestContext(request))

@permission_required('adzone.change_adbase')
def xhr_ad_table(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if (q is not None):
            imps = AdImpression.objects.filter(impression_date__gte=startdate, impression_date__lte=enddate)
            clicks = AdClick.objects.filter(click_date=startdate, click_date=enddate)
    return render_to_response('adzone/ad_index.html', locals(), context_instance=RequestContext(request))
