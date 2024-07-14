from django.db import models

from groceries.models.article import Article
from groceries.models.shop import Shop

class InvoiceLine(models.Model):
    # Purchased article
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    # total_spent 
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    # Unit Price
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Quantity
    quantity = models.IntegerField()
    # Date of purchase
    purchase_date = models.DateField()
    # Shop
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.id
    
    def __repr__(self):
        return self.id

    class Meta:
        ordering = ['id']
        verbose_name = "Invoice Line"
        verbose_name_plural = "Invoice Lines"