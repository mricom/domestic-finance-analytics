from ninja import NinjaAPI	
from ninja.security import django_auth
from groceries.api.analytics import router as analytics_router


API_PATH = 'api/v1/groceries/'

groceries_api = NinjaAPI(
    title='Groceries API',
    version='1.0.0',
    csrf=False, 
    urls_namespace=API_PATH
)

groceries_api.add_router('analytics', analytics_router)