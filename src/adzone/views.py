# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from adzone.models import AdBase, AdClick

def ad_view(request, id):
    """
    Record the click in the database, then redirect to ad url

    """
    ad = get_object_or_404(AdBase, id=id)
    try:
        if not request.excluded_ip:
            click = AdClick(
                ad=ad,
                click_date=datetime.now(),
                source_ip=request.META.get('REMOTE_ADDR')
            )
            click.save()
    except:
        pass
    return HttpResponseRedirect(ad.url)

def ad_display(request):
    """
    Simply pull an ad from the db and display it as a raw img.
    This was added to interface with legacy apps in iframes.
    Currently it's hardwired to calendar zone, but could be made scriptabled via GET params.
    """
    context=RequestContext(request)    
    ad = AdBase.objects.get_random_ad('', 'calendar')
    
    # Record a impression for the ad
    if context.has_key('from_ip') and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                    ad=ad,
                    impression_date=datetime.now(),
                    source_ip=from_ip
            )
            impression.save()
        except:
            pass
    
    return render_to_response('adzone/ad_display.html', locals(),
                          context_instance=RequestContext(request))
