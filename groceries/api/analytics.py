import datetime
from django.http import HttpResponse
from ninja import ModelSchema, Router, Schema
from django.db.models import Sum
from requests import HTTPError

from groceries.models.article import Article
from groceries.models.invoice_line import InvoiceLine

router = Router()


class ArticleSchema(ModelSchema):
    class Config:
        model = Article
        model_fields = "__all__"


class InputInvoiceLineSchema(Schema):
    shop_id: int
    cost: float


class InputInvoiceSchema(Schema):
    date: datetime.datetime
    lines: list[InputInvoiceLineSchema]


@router.get("/group_by/", response=dict)
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


@router.get("/price-ranking/", response=list[ArticleSchema])
def get_groceries_ranked_by_price(request, limit: int, date: str):
    """
    Returns the top [limit] most expensive items in a specific invoice.

    Query parameters:
    - limit: The number of items to return.
    - date: The date of the invoice.
    """
    invoice_lines = InvoiceLine.objects.filter(invoice__date=date).order_by(
        "-total_cost"
    )[:limit]
    return invoice_lines


@router.post("/invoice/")
def create_invoice(request, data: InputInvoiceSchema):
    """
    Create a new invoice.
    """
    invoice_exists = InvoiceLine.objects.filter(date=data.date).exists()
    if invoice_exists:
        return HTTPError(400, "Invoice already exists")
    try: 
        for line in data.lines:
            InvoiceLine.create_invoice_line(
                article_shop_id=line.shop_id, cost=line.cost, purchase_date=data.date
            )
    except Exception as e:
        return HTTPError(500, str(e))

    return HttpResponse(200, {"message": "Invoice created successfully!"})
