import requests 
import fake_useragent


def get_binance_rates(type='BUY', fiat='RUB', asset="USDT", pay='TinkoffNew', formats='s'):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    user = fake_useragent.UserAgent().random
    headers = {
        'accept': "*/*",
        'user-agent': user
    }
    
    params = {
        "asset": f"{asset}",
        "countries": [],
        "fiat": f"{fiat}",
        # "merchantCheck": False,
        "page": 1,
        "payTypes": [f"{pay}"],
        # "proMerchantAds": False,
        "publisherType": 'merchant',
        "rows": 10,
        "tradeType": f"{type}",
        # "transAmount": vol,
    }
        
    return requests.post(url=url, headers=headers, json=params).json()