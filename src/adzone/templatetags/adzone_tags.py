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
        excluded_ip = context.get('excluded_ip')
        if not excluded_ip:
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

@register.inclusion_tag('adzone/ad_tag_block.html', takes_context=True)
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
        lookup_ads=AdBase.objects.filter(enabled=True, category__slug=ad_category, zone__slug=ad_zone)
    else:
        lookup_ads=AdBase.objects.filter(enabled=True, zone__slug=ad_zone)

    # If we have fewer ads in system, adjust our block
    if len(lookup_ads) < number:
        number = len(lookup_ads)

    while(number > 0):
        new_ad= AdBase.objects.get_random_ad(ad_category, ad_zone)
        if new_ad in ads:
            pass
        else:
            ads.append(new_ad)
            number=number-1
        
            # Record a impression for the ad
            if new_ad:
                excluded_ip = context.get('excluded_ip')
                if not excluded_ip:
                    try:
                        impression = AdImpression(
                                ad=new_ad,
                                impression_date=datetime.now(),
                                source_ip=context.get('from_ip')
                                )
                        impression.save()
                    except:
                        pass
    to_return['ads'] = ads
    return to_return
