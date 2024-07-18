from ninja import ModelSchema, Router
from django.db.models import Sum

from groceries.models.article import Article
from groceries.models.invoice_line import InvoiceLine

router = Router()


class ArticleSchema(ModelSchema):
    class Meta:
        model = Article
        fields = [
            # "shop_id",
            # "name",
            # "long_name",
            # "description",
            # "brand",
            # "category",
            # "unit_price",
            # "is_available",
            # "in_promo",
            # "nutriscore",
            # "country_of_origin",
            # "is_bio",
            # "in_season",
        ]


@router.get("/group_by/")
def get_grouped_groceries_by_field(
    request, field: str = None, date: str = None
) -> list:
    """
    Returns the total cost of the invoice lines in a specific date grouped by the field provided.

    Query parameters:
    - field: The field to group by.
    - date: The date of the invoice.
    """
    # Gets the total cost of the invoice lines in a specific date grouped by the field provided.
    costs_list = list(
        InvoiceLine.objects.filter(purchase_date=date)
        .values(f"article__{field}")
        .annotate(total_cost=Sum("cost"))
    )
    total_cost_per_category = {
        item[f"article__{field}"]: item["total_cost"] for item in costs_list
    }
    return total_cost_per_category


@router.get("/price-ranking/", response=[ArticleSchema])
def get_groceries_ranked_by_price(request, limit: int, date: str):
    """
    Returns the top [limit] most expensive items in a specific invoice.

    Query parameters:
    - limit: The number of items to return.
    - date: The date of the invoice.
    """
    invoice_lines = InvoiceLine.objects.filter(invoice__date=date).order_by("-total_cost")[:limit]
    return invoice_lines
