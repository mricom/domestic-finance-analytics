from ninja import NinjaAPI	
from ninja.security import django_auth
from groceries.api.groceries import router as groceries_router


API_PATH = '/api/v1/groceries/'

groceries_api = NinjaAPI(
    title='Groceries API',
    version='1.0.0',
    api_path=API_PATH, 
    csrf=True, 
    auth=[django_auth]
)

groceries_api.add_router('groceries', groceries_router)