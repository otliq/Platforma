from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import script
import requests 
import fake_useragent
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import LoginUserForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    return render(request, 'index.html')

def terms(request):
    return render(request, 'termsandco.html')

def contact(request):
    return render(request, 'contact.html')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('results')
        
def logout_user(request):
    logout(request)
    return redirect('login')
    
#BINANCE
def get_data(fiat='RUB', asset="USDT", pay='TinkoffNew', type='SELL'):
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
        # "publisherType": 'merchant',
        "rows": 10,
        "tradeType": f"{type}",
        # "transAmount": vol,
    }

    try:
        response = requests.post(url=url, headers=headers, json=params)
        response.raise_for_status()  # проверяем статус код ответа
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)  # выводим сообщение об ошибке
        return {'error': 'Something went wrong'}

def get_garantex_rates(fiat='RUB', asset="USDT"):
    url = f'https://garantex.io/api/v2/depth?market={asset.lower()}{fiat.lower()}'
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
        print(e)  # выводим сообщение об ошибке
        return {'error': 'Something went wrong'}

#HUOBI
def get_rates_huobi(fiat='RUB', asset="USDT", pay='TinkoffNew', type='SELL'):
    url = f'https://www.huobi.com/-/x/otc/v1/data/trade-market'
    user = fake_useragent.UserAgent().random
    headers = {
        'accept': "*/*",
        'user-agent': user
    }
    pay_methods = {
        'TinkoffNew':28,
        'RosBankNew':29,
    }
    if pay in pay_methods:
        pay = pay_methods[pay]
    else:
        pay = 0
    cid = {
        'BTC':1,
        'ETH':3,
        'USDT':2
    }
    if asset in cid:
        asset = cid[asset]

    currency = {
        'RUB':11,
        'USD':2,
        'KGS':80,
        'UZS':61,
        'TRY':23,
        'KZT':57,
        'EUR':14,
        'CNY':172,
        'GBP':12,
        'CHF':9,
        'CAD':6,
        'AUD':7,
        'NZD':24,
        # 'KWD':102,
    }
    if fiat in currency:
        fiat = currency[fiat]

    payload = {
        'coinId': asset,
        'currency': fiat,
        'tradeType': f"{type.lower()}",
        'currPage': 1,
        'payMethod': pay,
        'acceptOrder': 0,
        # 'country': ,
        'blockType': 'general',
        'online': 1,
        'range': 0,
        # 'amount': ,
        'onlyTradable': 'false',
        'isFollowed': 'false'
        }
    try:
        response = requests.get(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data'][:10]
    except requests.exceptions.RequestException as e:
        print(e)  # выводим сообщение об ошибке
        return {'error': 'Something went wrong'}


# @csrf_exempt
def update_table(request, type='BUY', fiat='RUB', asset="USDT", pay='TinkoffNew'):
    # Получение параметров запроса
    if request.user.is_authenticated:
        fiat = request.POST.get('fiat')
        asset = request.POST.get('crypto')
        pay = request.POST.get('pay')
        type = request.POST.get('type')

        #Binance
        bid = get_data(fiat=fiat, asset=asset, pay=pay, type='SELL')
        ask = get_data(fiat=fiat, asset=asset, pay=pay, type='BUY')
        
        #Garantex
        fiat_lower = fiat.lower()
        asset_lower = asset.lower()
        garantex_fiat = ['rub','usd','eur']
        garantex_asset = ['usdt','btc','eth']
        link = asset_lower + fiat_lower

        #HUOBI
        hbids = get_rates_huobi(fiat=fiat, asset=asset, pay=pay, type='BUY')
        hasks = get_rates_huobi(fiat=fiat, asset=asset, pay=pay, type='SELL')

        if fiat_lower in garantex_fiat and asset_lower in garantex_asset:
            garantex = get_garantex_rates(fiat=fiat_lower, asset=asset_lower)
            gasks = garantex['asks'][:10]
            gbids = garantex['bids'][:10]
            return JsonResponse({'bid': bid, 'ask': ask, 'gasks':gasks, 'gbids':gbids, 'link':link, 'hbids':hbids, 'hasks':hasks})
        else:
            return JsonResponse({'bid': bid, 'ask': ask,'hbids':hbids, 'hasks':hasks})
    else:
        return HttpResponseForbidden()

def get_results(request):
    if request.user.is_authenticated:
        #binance
        ask = script.get_binance_rates(type='BUY')
        bid = script.get_binance_rates(type='SELL')
        
        #garantex
        fiat_lower = 'rub'
        asset_lowet = 'usdt'
        garantex = get_garantex_rates(fiat=fiat_lower, asset=asset_lowet)
        gasks = garantex['asks'][:10]
        gbids = garantex['bids'][:10]

        #HUOBI
        hbids = get_rates_huobi(type='BUY')
        hasks = get_rates_huobi(type='SELL')

        return render(request, 'base.html', {'bid': bid, 'ask': ask, 'gasks':gasks, 'gbids':gbids, 'hbids':hbids, 'hasks':hasks})
    else:
        return HttpResponseForbidden()


def pageNotFound(request, exception):
    return HttpResponseNotFound(
        "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;'><style>body {background-color: #000000;color: #eee;}a {color: #FFA500;}</style><title>Oops...</title><h1>Something went wrong</h1><p>Hello! If you want to login to your profile, please go to the login page, which you can find at the following link. There you can enter your username and password to access your profile. If you encounter any issues with logging in, please contact our support team. Thank you!</p><p><a href='/' style='text-align:center;'>Login</a></p></div>"
    )
    

def delete_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=31)
    inactive_users = User.objects.filter(is_active=True, date_joined__lt=one_month_ago)
    inactive_users.delete()
    
# class PlatformaRatesView(APIView):
#     def get(self, request):
#         type = request.GET.get('type', 'BUY')
#         fiat = request.GET.get('fiat', 'RUB')
#         asset = request.GET.get('asset', 'USDT')
#         pay = request.GET.get('pay', 'TinkoffNew')

#         response = get_data(type=type, fiat=fiat, asset=asset, pay=pay)
#         prices = []
#         volumes = []
#         # links = []
#         try:
#             data = response['data'][:10]
#             for item in data:
#                 price = float(item['adv']['price'])
#                 prices.append(price)
#                 volume = float(item['adv']['tradableQuantity'])
#                 volumes.append(volume)
#                 # userno = item['advertiser']['userNo']
#                 # link = f"https://p2p.binance.com/en/advertiserDetail?advertiserNo={userno}"
#                 # links.append(link)
                
#             rates = {
#                 'prices': prices,
#                 'volumes': volumes,
#                 # 'links': links,
#             }
            
#             return Response(rates)
            
#         except KeyError:
#             return Response({'error': 'API response is missing required data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

