from django.core.management.base import BaseCommand
from groceries.models import Article
from groceries.utils.preprocessing import parse_price
from groceries.utils.scrapper import scrap_colruyt_data
import numpy as np, pandas as pd

class Command(BaseCommand):
    help = 'Populate the products database with data from scrapped from colruyt'

    
    def handle(self, *args, **kwargs):
        field_mapping = {
        'commercialArticleNumber': 'shop_id',
        'name': 'name',
        'LongName': 'long_name',
        'brand': 'brand',
        'topCategoryName': 'category',
        'content': 'content',
        'unit_price': 'unit_price',
        'isAvailable': 'is_available',
        'inPromo': 'in_promo',
        'nutriscoreLabel': 'nutriscore',
        'CountryOfOrigin': 'country_of_origin',
        'IsBio': 'is_bio',
        'IsNew': 'is_new',
        'InSeason': 'in_season',
        'StartSeasonDate': 'season_start_date'
    }
        scrapped_data = scrap_colruyt_data()
        scrapped_data['commercialArticleNumber'] = scrapped_data['commercialArticleNumber'].astype(int)
        scrapped_data['unit_price'] = parse_price(scrapped_data['price'])
        scrapped_data = scrapped_data.rename(columns=field_mapping)[field_mapping.values()]
        scrapped_data = scrapped_data.replace({np.nan:None}) # Models will not accept np NaN values
        scrapped_data['season_start_date'] = pd.to_datetime(scrapped_data['season_start_date'], format='%d/%m/%Y', errors='coerce')
        scrapped_data['season_start_date'] = scrapped_data['season_start_date'].astype(object).where(scrapped_data['season_start_date'].notnull(), None)
        scrapped_data['category'] = scrapped_data['category'].fillna('Unknown')
        scrapped_data = scrapped_data.drop_duplicates(subset=['shop_id'])

        for _, row in scrapped_data.iterrows():
            Article.objects.create(**row.to_dict())
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))