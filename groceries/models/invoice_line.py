from django.db import models

from groceries.models.article import Article
from groceries.models.shop import Shop
from groceries.utils.errors.errors import NotFoundException

KNOWN_STORES = {
    639: {
        "id": 1, 
        "name": "Colruyt St-Katelijne-Waver",
        "location": "St-Katelijne-Waver",
    }, 
    683: {
        "name": "Colruyt Mechelen",
        "location": "Mechelen",
    },
}

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
    purchase_date = models.DateTimeField()
    # Shop
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)

    def __str__(self):
        return self.article.name

    def __repr__(self):
        return self.article.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Invoice Line"
        verbose_name_plural = "Invoice Lines"

    @classmethod
    def create_invoice_line(cls, article_shop_id, cost, purchase_date, shop_id=None):
        if shop_id:
            shop = Shop.objects.filter(id=shop_id).first()
            if not shop and shop_id in list(KNOWN_STORES.keys()):
                shop = Shop.objects.create(
                    id=KNOWN_STORES[shop_id]["id"],
                    name=KNOWN_STORES[shop_id]["name"],
                    location=KNOWN_STORES[shop_id]["location"],
                    shop_id=shop_id,
                )
        if not shop:
            raise NotFoundException("No shop found in the database.")
        shop_id = shop.id
        article = Article.objects.filter(shop_id=article_shop_id).first()
        if not article:
            raise NotFoundException(f"No article found in the database with article id: {article_shop_id}.")
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
