import pandas as pd, numpy as np
import tabula

def preprocess_scrapped_products(scrapped_data: pd.DataFrame):
    
    return scrapped_data

def get_table():
    scanned_prices = scan_prices(get_mock_last_data())
    products = pd.read_csv('products_f.csv')
    products['commercialArticleNumber'] = products['commercialArticleNumber'].astype(int)
    scanned_info = scanned_prices.merge(products, how='left', left_on='article_id', right_on='commercialArticleNumber')
    scanned_info['commercialArticleNumber'] = scanned_info['commercialArticleNumber'].fillna(scanned_info['article_id']).astype(int)
    scanned_info.loc[scanned_info['technicalArticleNumber'].isna(), 'name'] = '[CANNOT MAP] possibly tobacco'
    scanned_info['unit_price'] = parse_price(scanned_info['price'])
    #info = scanned_info.groupby('categories').total_spent.sum().reset_index().sort_values(by='total_spent', ascending=False)
    return scanned_info

min_id_prod = 1000

def get_mock_last_data():
    return tabula.read_pdf("test.pdf", pages='all')


def get_article_id(df_raw):
    try:
        article_ids_descrp_col = df_raw['Unnamed: 0'].str.extract(r'(\d+|Réduction)').replace('0', np.nan).replace('Réduction', 999999999).dropna().rename(columns={0: 'article_id'}).astype(int)
        article_ids_descrp_col = article_ids_descrp_col.query("article_id >= @min_id_prod")
        article_ids_validation_col = df_raw['T'].str.extract(r'(\d+|Réduction)').replace('0', np.nan).dropna().rename(columns={0: 'article_id'}).astype(int)
        article_ids_validation_col = article_ids_validation_col.query("article_id >= @min_id_prod")
        
        article_ids = article_ids_descrp_col if article_ids_descrp_col.shape[0] > article_ids_validation_col.shape[0] else article_ids_validation_col
        article_ids = pd.DataFrame() if article_ids.shape[0] < int(df_raw.shape[0]/3) else article_ids
        return article_ids
    except KeyError as e:
        print(f"Error: {e}")
        print(" Returning empty dataframe")
        return pd.DataFrame()

def get_total_price(df_raw):
    try:
        source_info_col = 'Unnamed: 4'
        if not 'Unnamed: 4' in df_raw.columns:
            source_info_col = 'Unnamed: 3'
            df_raw = df_raw.dropna(subset=[source_info_col])
            df_raw = df_raw[~df_raw[source_info_col].str.contains('€')] # filter out totals from transactions
        df_raw = df_raw[df_raw[source_info_col].str.contains('\d', na=False)]
        # Rename columns and convert to numeric
        return df_raw[source_info_col].str.replace(',', '.').str.extract(r'(-?\d+\.\d+)$').astype(float).dropna().rename(columns={0: 'total_spent'})
    except KeyError as e:
        print(f"Error: {e}")
        print(" Returning empty dataframe")
        return pd.DataFrame()

def scan_prices(dfs: list):
    scanned_prices = pd.DataFrame()
    for df in dfs:
        ids = get_article_id(df)
        prices = get_total_price(df)
        extracted_info = pd.merge(ids, prices, left_index=True, right_index=True) # inner join will take care of removing rubbish
        scanned_prices = pd.concat([scanned_prices, extracted_info], ignore_index=True)

    return scanned_prices

def parse_price(price: pd.Series):
    return price.apply(lambda x: x['basicPrice'] if not pd.isna(x) else np.nan).astype(float)