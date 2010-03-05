# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib import admin
from adzone.models import Advertiser, AdCategory, AdZone, TextAd, BannerAd, FlashAd, AdClick, AdImpression, PaperAd

class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']

admin.site.register(Advertiser, AdvertiserAdmin)

class AdZoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description']

admin.site.register(AdZone, AdZoneAdmin)

class TextAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url', 'content']

admin.site.register(TextAd, TextAdAdmin)

class PaperAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url', 'content']

admin.site.register(PaperAd, PaperAdAdmin)

class BannerAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url']

admin.site.register(BannerAd, BannerAdAdmin)

class FlashAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url']

admin.site.register(FlashAd, FlashAdAdmin)

class AdClickAdmin(admin.ModelAdmin):
    pass

admin.site.register(AdClick, AdClickAdmin)

class AdImpressionAdmin(admin.ModelAdmin):
    pass

admin.site.register(AdImpression, AdImpressionAdmin)

admin.site.register(AdCategory)






