from ninja import NinjaAPI	
from ninja.security import django_auth
from groceries.api.analytics import router as analytics_router
from groceries.utils.errors.errors import AlreadyExistsException, GenericException, NotFoundException


API_PATH = 'api/v1/groceries/'

groceries_api = NinjaAPI(
    title='Groceries API',
    version='1.0.0',
    csrf=False, 
    urls_namespace=API_PATH
)

groceries_api.add_router('analytics', analytics_router)

@groceries_api.exception_handler(GenericException)
def generic_exception(request, exc):
    return groceries_api.create_response(request, {"message": exc.message}, status=500)

@groceries_api.exception_handler(AlreadyExistsException)
def already_exists_exception(request, exc):
    return groceries_api.create_response(request, {"message": exc.message}, status=400)

@groceries_api.exception_handler(NotFoundException)
def not_found_exception(request, exc):
    return groceries_api.create_response(request, {"message": exc.message}, status=404)