from ninja import ModelSchema, Router

from groceries.models.article import Article

router = Router()

class ArticleSchema(ModelSchema): 
    class Meta:
        model = Article
        fields = '__all__'

@router.get('/group_by/')
def get_grouped_groceries_by_field(request, field: str, date: str):
    """
    Returns the total cost of the items grouped by the field provided in a specific date.
    """ 
    pass

@router.get('/price-ranking/', response=[ArticleSchema])
def get_groceries_ranked_by_price(request, limit: int, date: str):
    """
    Returns the top [limit] most expensive items in a specific invoice. 
    """
    pass

