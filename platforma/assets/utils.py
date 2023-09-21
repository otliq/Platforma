import json
import requests 
import fake_useragent
from django.http import JsonResponse, HttpResponseForbidden, HttpRequest, HttpResponse

# Constants are necessary to make the correct request to exchanges
from .constants import huobi_currencys, huobi_cid, huobi_pay_methods

def get_binance_rates(fiat:str = 'USD', 
                      asset:str = "USDT", 
                      pay:str = 'Wise', 
                      type:str = 'SELL') -> json:
    """
    Функция для получения данных с биржи BINANCE.
    Каждый запрос отправляется с разных агентов во избежании блокировок со стороны биржи.

    Особенности:
        не поддерживает только фиатную валюту RUB и связанные с ним методы платежа
    """
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
        "page": 1,
        "payTypes": [f"{pay}"],
        "rows": 10,
        "tradeType": f"{type}",
    }
    try:
        response = requests.post(url=url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error': 'Something went wrong'}

def get_garantex_rates(fiat:str = 'USD', 
                       asset:str = "USDT") -> json:
    """
    Функция для получения данных с биржи GARANTEX.
    Каждый запрос отправляется с разных агентов во избежании блокировок со стороны биржи.

    Особенности:
        поддерживает только 3 актива [BTC, ETH, USDT]
        поддерживает только 2 фиатной валюты [USD, RUB]
    """
    url = f'https://garantex.org/api/v2/depth?market={asset.lower()}{fiat.lower()}'
    user = fake_useragent.UserAgent().random
    headers = {
        'accept': "*/*",
        'user-agent': user
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error': 'Something went wrong'}

def get_huobi_rates(fiat:str = 'USD', 
                    asset:str = "USDT", 
                    pay:str = 'TinkoffNew', 
                    type:str = 'SELL') -> json:
    """
    Функция для получения данных с биржи HUOBI.
    Каждый запрос отправляется с разных агентов во избежании блокировок со стороны биржи.

    Особенности:
        поддерживает только 3 актива [BTC, ETH, USDT]
        стабильно поддерживает только 2 фиатной валюты [USD, RUB]
    """
    url = f'https://www.huobi.com/-/x/otc/v1/data/trade-market'
    user = fake_useragent.UserAgent().random
    headers = {
        'accept': "*/*",
        'user-agent': user
    }

    if pay in huobi_pay_methods:
        pay = huobi_pay_methods[pay]
    else:
        pay = 28
    if asset in huobi_cid:
        asset = huobi_cid[asset]
    if fiat in huobi_currencys:
        fiat = huobi_currencys[fiat]
    payload = {
        'coinId': asset,
        'currency': fiat,
        'tradeType': f"{type.lower()}",
        'currPage': 1,
        'payMethod': pay,
        'acceptOrder': 0,
        'blockType': 'general',
        'online': 1,
        'range': 0,
        'onlyTradable': 'false',
        'isFollowed': 'false'
        }
    try:
        response = requests.get(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data'][:10]
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error': 'Something went wrong'}

def update_table(request: HttpRequest, 
                 fiat: str='USD', 
                 asset: str="USDT", 
                 pay: str='Wise') -> HttpResponse:
    """
    Функция-обработчик для AJAX запросов со страницы.
    
    Основная задача:
        Собрать данные со всех бирж
        Передать их в виде JSON на главную страницу
    """
    if request.user.is_authenticated:
        fiat = request.POST.get('fiat')
        asset = request.POST.get('crypto')
        pay = request.POST.get('pay')

        #Binance
        bid = get_binance_rates(fiat=fiat, asset=asset, pay=pay, type='SELL')
        ask = get_binance_rates(fiat=fiat, asset=asset, pay=pay, type='BUY')
        
        #Garantex
        fiat_lower = fiat.lower()
        asset_lower = asset.lower()
        garantex_fiat = ['rub','usd','eur']
        garantex_asset = ['usdt','btc','eth']
        link = asset_lower + fiat_lower

        #HUOBI
        hbids = get_huobi_rates(fiat=fiat, asset=asset, pay=pay, type='BUY')
        hasks = get_huobi_rates(fiat=fiat, asset=asset, pay=pay, type='SELL')

        if fiat_lower in garantex_fiat and asset_lower in garantex_asset:
            garantex = get_garantex_rates(fiat=fiat_lower, asset=asset_lower)
            gasks = garantex['asks'][:10]
            gbids = garantex['bids'][:10]
            return JsonResponse({'bid': bid, 
                                 'ask': ask, 
                                 'gasks':gasks, 
                                 'gbids':gbids, 
                                 'link':link, 
                                 'hbids':hbids, 
                                 'hasks':hasks})
        else:
            return JsonResponse({'bid': bid, 
                                 'ask': ask,
                                 'hbids':hbids, 
                                 'hasks':hasks})
    else:
        return HttpResponseForbidden()