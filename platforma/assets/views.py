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
    delete_inactive_users()
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
    


def get_data(fiat='RUB', asset="USDT", pay='TinkoffNew', type='SELL', vol=15000):
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

    try:
        response = requests.post(url=url, headers=headers, json=params)
        response.raise_for_status()  # проверяем статус код ответа
        return response.json()
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
        
        bid = get_data(fiat=fiat, asset=asset, pay=pay, type='SELL')
        ask = get_data(fiat=fiat, asset=asset, pay=pay, type='BUY')
        
        return JsonResponse({'bid': bid, 'ask': ask})
    else:
        # пользователь не авторизован, возвращаем ошибку 403 Forbidden
        return HttpResponseForbidden()


def get_results(request):
    if request.user.is_authenticated:
        ask = script.get_binance_rates(type='BUY')
        bid = script.get_binance_rates(type='SELL')
        return render(request, 'base.html', {'bid': bid, 'ask': ask})
    else:
        # пользователь не авторизован, возвращаем ошибку 403 Forbidden
        return HttpResponseForbidden()


def pageNotFound(request, exception):
    return HttpResponseNotFound(
        "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;'><style>body {background-color: #000000;color: #eee;}a {color: #FFA500;}</style><title>Oops...</title><h1>Something went wrong</h1><p>Hello! If you want to login to your profile, please go to the login page, which you can find at the following link. There you can enter your username and password to access your profile. If you encounter any issues with logging in, please contact our support team. Thank you!</p><p><a href='/' style='text-align:center;'>Login</a></p></div>"
    )
    

def delete_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=31)
    inactive_users = User.objects.filter(is_active=True, date_joined__lt=one_month_ago)
    inactive_users.delete()
    
class PlatformaRatesView(APIView):
    def get(self, request):
        type = request.GET.get('type', 'BUY')
        fiat = request.GET.get('fiat', 'RUB')
        asset = request.GET.get('asset', 'USDT')
        pay = request.GET.get('pay', 'TinkoffNew')

        response = get_data(type=type, fiat=fiat, asset=asset, pay=pay)
        prices = []
        volumes = []
        # links = []
        try:
            data = response['data'][:10]
            for item in data:
                price = float(item['adv']['price'])
                prices.append(price)
                volume = float(item['adv']['tradableQuantity'])
                volumes.append(volume)
                # userno = item['advertiser']['userNo']
                # link = f"https://p2p.binance.com/en/advertiserDetail?advertiserNo={userno}"
                # links.append(link)
                
            rates = {
                'prices': prices,
                'volumes': volumes,
                # 'links': links,
            }
            
            return Response(rates)
            
        except KeyError:
            return Response({'error': 'API response is missing required data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)