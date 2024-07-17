from django.db import models
from groceries.models.shop import Shop

class Article(models.Model):
    # Id of the article in the shop (article_id)
    shop_id = models.BigIntegerField()
    # Short name
    name = models.CharField(max_length=255, null=True, blank=True)
    # Long name
    long_name = models.CharField(max_length=400, null=True, blank=True)
    # Description
    description = models.TextField(null=True, blank=True)
    # Brand
    brand = models.CharField(max_length=255, null=True, blank=True)
    # TODO: Check!!
    # Category
    category = models.CharField(max_length=100, default="Unknown")
    # Content
    content = models.CharField(max_length=50, null=True, blank=True)
    # Basic Price
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # isAvailable
    is_available = models.BooleanField(default=True, blank=True)
    # inPromo
    in_promo = models.BooleanField(default=False, blank=True, null=True)
    # nutriscoreLabel
    nutriscore = models.CharField(max_length=1, null=True, blank=True)
    # countryOfOrigin
    country_of_origin = models.CharField(max_length=100, null=True, blank=True)
    # isBio
    is_bio = models.BooleanField(null=True, blank=True)
    # isNew
    is_new = models.BooleanField(null=True, blank=True)
    # inSeason
    in_season = models.BooleanField(null=True, blank=True)
    # startSeasonDate
    season_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.long_name
    
    def __repr__(self):
        return self.long_name

    class Meta: 
        ordering = ['id']
        verbose_name = "Article"
        verbose_name_plural = "Articles"