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
            #"Cookie": "TS015e04f8=016303f95576d363f55059a3a3818772114570fd3b8228c6df1dda315e32500ddd359c62aa01e34cbd24688fba9102c2ac19765c23; rxVisitor=172052377001222RHPLKOVEMGVNI2DCU3VEFHC76MRTQJ; AMCVS_FA4C56F358B81A660A495DE5%40AdobeOrg=1; s_ecid=MCMID%7C19090225063546995330109051806389726665; s_cc=true; OptanonAlertBoxClosed=2024-07-09T11:19:22.741Z; at_check=true; _tt_enable_cookie=1; _ttp=TH8bGX7oYkqjJJg-lyMIGbzUpjJ; _pin_unauth=dWlkPU4yTXhaak5pTVRjdFlXSmhaaTAwTjJFNExUZ3lNV0l0WlRZeFlqVm1Oekl4T1dJeQ; _hjSessionUser_137278=eyJpZCI6ImQzZjEyYjkyLWU2YzEtNWJhNi1hMTE0LTE1NWRkMTgzZWMzMSIsImNyZWF0ZWQiOjE3MjA1MjM5NjM5MjcsImV4aXN0aW5nIjp0cnVlfQ==; bff_session=3431ee98-a2d7-4c08-9247-5aefc803c44d; TS0114f963=016303f955e6aad5fe8a5b022fde9d76e857fa7482a8815744de729dea10d721bd5b589f0dcb3dd4bcf7c9bdbf1d063f96c819e5c5; dtSa=-; rxvt=1720897326383|1720895333276; dtPC=21$95525947_377h-vPDHBQEMCBRHAVKHWSUHSQUJVDQVLKGSR-0e0; TS01461a64=016303f95512f2993d50ddbac1eafc41b2fa9abdb545f5046ac6c750af19849e6074f985f5eba7af48dd792b342a8bcd2528956020; dtCookie=v_4_srv_19_sn_3A5AF60BC19352F914BAB8E0DC6A42F7_perc_100000_ol_0_mul_1_app-3Ab84fed97a8123cd5_0; _gcl_au=1.1.1941662676.1720523964.881225757.1720983132.1720983132; AMCV_FA4C56F358B81A660A495DE5%40AdobeOrg=1406116232%7CMCIDTS%7C19921%7CMCMID%7C19090225063546995330109051806389726665%7CMCAAMLH-1721729055%7C6%7CMCAAMB-1721729055%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1721131455s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.5.0; _hjSession_137278=eyJpZCI6IjI4NjUzMTAwLTY3ZmYtNGUxNS05ODRjLWJmYjkyNWZjNTNlYSIsImMiOjE3MjExMjQyNTg3NTEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; mboxEdgeCluster=37; _uetsid=c3df7090435a11ef92867dcb8caeb3a6; _uetvid=1826eb203de511ef8adb57286877b886; reese84=3:vj5z7/uWW457RW5CtuEOQQ==:zwrYT911gbHn41VJSf0a1AeX/5OJ2wiiXAsv1uiFsswKVSTkBsc5EWmB+PMmidx4w/PEvvjx2fvQ1FA87Ntl5qBWWkkH+lEb9vMlkzy9E3OOYu2hh9zBCKJfF509qMZd+lFHaZzWRoQJofEdI33YhDi+F6LC0KGUqHER5YVDHG7fuO/zsTMAgTh/0v+azOi79lQqyAlJoHJY53i8bWE+D4WN4QsbK7rptqzQDwieefv/Rbpl1b+eamlnjNEHP5IZbhTJeGh6JsWhdjVEZ+haOmjRSVNYhC4Zb7Gpv9nsBUGvlSN+0LYrEPJ0GDet5nqBEGGTSXkE9aVcWsS60Fn8d+TljaGvWuhXNRssxmLFdY9LsJ7CBgTqq5JrG/2ra+tvtcgFKCn1orP42Rl03rR21NyPq8ccrrOabzWvvCI9ln6XIVe8oSwgy1jR9S6Ks/UR5q9o1S0Bc6Pe2+0oFe95iA==:aLTokju7ZUVadh3SMLGHdPnFNtuZN7GVgUGklH8GtMs=; mbox=PC#59a66176b97340f3b7bc2b0845e06075.37_0#1784371798|session#c28413fdc8df4aaba6a10640b951c560#1721128858; tms_storevisit=eyJ0aW1lRXZlbnRfbXNGb2N1c291dCI6MTQzODQwNTA4LCJ0aW1lRXZlbnRfc3RhcnRUaW1lIjoxNzIxMTI0MjU1NDk0LCJhZGJsb2NrX3N0YXR1cyI6Im5vdGFjdGl2ZSIsInBhZ2VfZGVwdGgiOjIsImJzbF9hcnRpY2xlX2NvdW50IjowLCJ1c2VyX3Zpc2l0X2lkIjoiMTkyMzg5LjE3MjExMjQyNTgxMDUiLCJhdF9jYmhfaWQiOiIyNzEyNzA0MiIsImxhc3RfbG9naW5fc3RhdGUiOiJ5ZXMifQ%3D%3D; utag_main=v_id:019097382f5b00162dca183aa38205075001906d01328$_sn:9$_se:4$_ss:0$_st:1721128797301$vapi_domain:colruyt.be$dc_visit:9$ses_id:1721126323113%3Bexp-session$_pn:2%3Bexp-session$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+16+2024+12%3A49%3A57+GMT%2B0200+(Central+European+Summer+Time)&version=6.20.0&isIABGlobal=false&hosts=&consentId=49232993-1fae-4bbb-8502-24b3d5a21cf4&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false"

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

    