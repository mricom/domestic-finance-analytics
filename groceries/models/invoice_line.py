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
        ordering = ["id"]
        verbose_name = "Invoice Line"
        verbose_name_plural = "Invoice Lines"

    @classmethod
    def create_invoice_line(cls, article_shop_id, cost, purchase_date, shop_id=None):
        shop = Shop.objects.first()
        if not shop:
            raise ValueError("No shop found in the database.")
        shop_id = shop.id
        article = Article.objects.filter(shop_id=article_shop_id).first()
        unit_price = article.unit_price
        quantity = int(cost / unit_price)

        invoice_line = cls.objects.create(
            article=article,
            cost=cost,
            unit_price=unit_price,
            quantity=quantity,
            purchase_date=purchase_date,
            shop_id=shop_id,
        )
        return invoice_line
