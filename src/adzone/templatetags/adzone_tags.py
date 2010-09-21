# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django import template
from adzone.models import AdBase, AdImpression
from datetime import datetime

register = template.Library()

@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_zone_ad(context, ad_category, ad_zone):
    """
    Returns a random advert from the database.

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'adzone.context_processors.get_source_ip'

    Tag usage:
    {% load adzone_tags %}
    {% random_zone_ad 'my_category_slug' 'zone_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    ad = AdBase.objects.get_random_ad(ad_category, ad_zone)
    to_return['ad'] = ad
    
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
    return to_return

@register.inclusion_tag('adzone/ads_tag_block.html', takes_context=True)
def random_zone_ad_block(context, ad_category, ad_zone, number):
    """
    Returns a block of random adverts from the database.

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'adzone.context_processors.get_source_ip'

    Tag usage:
    {% load adzone_tags %}
    {% random_zone_ad_block 'my_category_slug' 'zone_slug' 4 %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    ads=[]

    # Check whether category has been specified
    if ad_category:
        ads=AdBase.objects.filter(enabled=True, category=ad_category, zone=ad_zone)
    else:
        ads=AdBase.objects.filter(enabled=True, zone=ad_zone)

    # If we have fewer ads in system, adjust our block
    if len(ads) < number:
        number = len(ads)

    while(number > 0):
        new_ad= AdBase.objects.get_random_ad(ad_category, ad_zone)
        if new_ad in ads:
            pass
        else:
            ads.append(new_ad)
            n=n-1
        
    to_return['ads'] = ads
    
    # Record a impression for the ad
    if context.has_key('from_ip') and len(ads) != 0:
        for ad in ads:
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
    return to_return
