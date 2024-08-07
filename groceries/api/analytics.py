import datetime
import decimal
from django.http import JsonResponse
from ninja import ModelSchema, Router, Schema
from django.db.models import Sum
from typing import List

from groceries.models.article import Article
from groceries.models.invoice_line import InvoiceLine
import logging as logger

from groceries.utils.errors.errors import AlreadyExistsException, GenericException, NotFoundException

router = Router()


class ArticleSchema(ModelSchema):
    class Config:
        model = Article
        model_fields = "__all__"


class InputInvoiceLineSchema(Schema):
    shop_id: int
    cost: decimal.Decimal


class InputInvoiceSchema(Schema):
    date: datetime.datetime
    lines: List[InputInvoiceLineSchema]


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

@router.get("/price-ranking/", response=List[ArticleSchema])
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


@router.post("invoice/")
def create_invoice(request, data: InputInvoiceSchema):
    """
    Creates a new invoice.
    Check that there are no products that were already invoiced on the same date.
    """
    invoice_exists = InvoiceLine.objects.filter(purchase_date=data.date).exists()
    print(invoice_exists)
    if invoice_exists:
        raise AlreadyExistsException(message="Invoice already exists.")
    errors: list[str] = []
    try: 
        for line in data.lines:
            InvoiceLine.create_invoice_line(
                article_shop_id=line.shop_id, cost=line.cost, purchase_date=data.date
            )
    except AlreadyExistsException as e:
        logger.error(str(e))
        errors.append(str(e))
        # raise AlreadyExistsException(message=str(e))
    except NotFoundException as e:
        logger.error(str(e))
        errors.append(str(e))
        # raise NotFoundException(message=str(e))
    except Exception as e:
        logger.error(str(e))
        errors.append(str(e))
        # raise GenericException(message=str(e))
    raise GenericException(message=", ".join(errors))
    # return JsonResponse(200, {"message": "Invoice created successfully!"})
