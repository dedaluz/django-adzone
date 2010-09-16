from django.db import models

class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_category, ad_zone):
        """
        Returns a random advert that belongs to the specified category and zone
        
        """
	if ad_category=='':
            try:
                ad = self.get_query_set().filter(zone__slug=ad_zone).order_by('?')[0]
            except IndexError:
                return None;
        else:
            try:
                ad = self.get_query_set().filter(category__slug=ad_category, zone__slug=ad_zone).order_by('?')[0]
            except IndexError:
                return None;

        return ad
