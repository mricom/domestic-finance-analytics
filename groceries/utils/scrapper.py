import requests
import pandas as pd

def get_json_from_api(url, headers=None):
    try:
        response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None
   
def scrap_colruyt_data():
    scrapped_df = pd.DataFrame()
    i=1
    previous_buf = 0
    while True:
        print(i)
        print(scrapped_df.shape)
        try:
            api_url = f"https://apip.colruyt.be/gateway/emec.colruyt.protected.bffsvc/cg/fr/api/products?placeId=639&page={i}&size=250&isAvailable=true"
            headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-CG-APIKey": "a8ylmv13-b285-4788-9e14-0f79b7ed2411",

        }

            json_data = get_json_from_api(api_url, headers=headers)
            if not json_data :
                break
            scrapped_df = pd.concat([pd.DataFrame(json_data['products']), scrapped_df])
            if scrapped_df.shape[0] == previous_buf:
                break
            previous_buf = scrapped_df.shape[0]
            i += 1
            
        except:
            break
    return scrapped_df

    