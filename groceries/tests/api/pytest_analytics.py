import datetime
import math
import random
import pytest

from groceries.models.article import Article
from groceries.models.invoice_line import InvoiceLine
from groceries.models.shop import Shop
from groceries.api.analytics import get_groceries_ranked_by_price, get_grouped_groceries_by_field


@pytest.mark.django_db
@pytest.fixture
def create_shop():
    Shop.objects.create(name="Test Shop", location="Test Location", id=1)


@pytest.mark.django_db
@pytest.fixture
def create_articles():
    for i in range(1, 8):
        batch = math.ceil(i / 2)
        Article.objects.create(
            shop_id=i,
            name=f"Test {i}",
            brand=f"Test {batch}",
            category=f"Test {batch}",
            content=f"Test {i}",
            unit_price=i,
            is_available=True if i % 2 == 0 else False,
            in_promo=True if i % 2 == 0 else False,
            country_of_origin=f"Test {batch}",
        )

@pytest.mark.django_db
@pytest.fixture
def create_invoice_lines():
    articles = Article.objects.all()

    for article in articles:
        InvoiceLine.create_invoice_line(
            article_shop_id=article.shop_id,
            cost=article.unit_price,
            purchase_date="2021-01-01",
            shop_id=1,
        )


@pytest.mark.django_db
@pytest.mark.usefixtures("create_shop", "create_articles", "create_invoice_lines")
@pytest.mark.parametrize("field", ["category", "country_of_origin", "brand"])
def test_can_get_grouped_groceries_by_field(rf, field):
    costs = get_grouped_groceries_by_field(
        rf, field=field, date="2021-01-01"
    )
    print(costs)
    assert isinstance(costs, dict)
    assert costs["Test 1"] == 3
    assert costs["Test 2"] == 7
    assert costs["Test 3"] == 11
    assert costs["Test 4"] == 7


@pytest.mark.django_db
@pytest.mark.usefixtures("create_shop", "create_articles", "create_invoice_lines")
def test_can_get_groceries_ranked_by_price(rf):
    ranked_articles = get_groceries_ranked_by_price(rf, limit=3, date="2021-01-01")
    assert len(ranked_articles) == 3
    assert ranked_articles[0].unit_price == 7
    assert ranked_articles[1].unit_price == 6
    assert ranked_articles[2].unit_price == 5
