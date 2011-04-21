#! /usr/bin/env python
# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-
import logging
from datetime import datetime 
from django.db.models import Q
import django.utils.simplejson as json
import operator
from django.shortcuts import render_to_response 
from django.shortcuts import get_object_or_404 
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from django.template import RequestContext 
from django.contrib.auth.decorators import permission_required 
from django.core import serializers 
from adzone.models import AdBase, AdClick, BannerAd, TextAd, AdImpression

def ad_view(request, id):
    """
    Record the click in the database, then redirect to ad url

    """
    ad = get_object_or_404(AdBase, id=id)
    logging.debug('Found ad: %s, redirecting...' % (ad))
    try:
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
    from_ip = request.META['REMOTE_ADDR']
    if not request.excluded_ip:
        impression = AdImpression(ad=ad, impression_date=datetime.now(), source_ip=from_ip)
        impression.save()
    return render_to_response('adzone/ad_display.html', locals(), context_instance=RequestContext(request))


def _convert_string(date):
    if date == "Today":
        return datetime.now().strftime('%Y-%m-%d')
    elif date == "Yesterday":
        return (datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        return date

@permission_required('adzone.change_adbase')
def ad_index(request):
    ad_list=[]
    if request.method == 'GET':
        filter=[]
    if 'start' in request.GET:
        start = _convert_string(request.GET.get('start'))
        filter.append(start)
    if 'end' in request.GET:
        end = _convert_string(request.GET.get('end'))
        ads = AdBase.objects.enabled()
        for ad in ads:
            ad_list.append([ad, ad.impressions(*filter), ad.clicks(*filter)])
    else:
        ads = AdBase.objects.enabled()  
        for ad in ads:
            ad_list.append([ad, ad.impressions(), ad.clicks()])
    return render_to_response('adzone/ad_index.html', locals(), context_instance=RequestContext(request))

def ad_detail(request, id):
    ad=AdBase.objects.get(pk=id)
    return render_to_response('adzone/ad_detail.html', locals(), context_instance=RequestContext(request))

@permission_required('adzone.change_adbase')
def xhr_ad_detail(request, id, format=None):
    if request.is_ajax():
        if request.method == 'POST':
            filter=[]
            if 'start' in request.POST:
                start = _convert_string(request.POST.get('start'))
                filter.append(start)
            if 'end' in request.POST:
                end = _convert_string(request.POST.get('end'))
                ads = AdBase.objects.enabled()
                for ad in ads:
                    ad_list.append([ad, ad.impressions(*filter), ad.clicks(*filter)])
        else:
            ads = AdBase.objects.enabled()  
            for ad in ads:
                ad_list.append([ad, ad.impressions(), ad.clicks()])
        if format == 'json':
            mimetype='application/json'
        if format == 'xml':
            mimetype='application/xml'
        data = serializers.serialize(format, ads)
    else:
        return HttpResponse(status=400)
    return HttpResponse(data, mimetype)

@permission_required('adzone.change_adbase')
def xhr_ad_table(request, format=None):
    if request.is_ajax():
        ad_list=[]
        if request.method == 'POST':
            ads = AdBase.objects.enabled()
        if format == 'json':
            mimetype='application/json'
        if format == 'xml':
            mimetype='application/xml'
        if format == 'html':
            mimetype='text/html'
	data = serializers.serialize(format, ads)
    return HttpResponse(data, mimetype)
