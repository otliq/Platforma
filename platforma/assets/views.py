from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import LoginUserForm
from .utils import get_binance_rates, get_garantex_rates, get_huobi_rates

class LoginUser(LoginView):
    """
    View для входа пользователя в систему.
    После успешного входа пользователь будет перенаправлен на осноную страницу.
    """
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('results')

def index(request: HttpRequest) -> HttpResponse:
    """
    View для главной страницы.
    """
    return render(request, 'index.html')

def logout_user(request: HttpRequest) -> HttpResponse:
    """
    Выход пользователя из системы.
    Возвращает: HTTP-ответ, перенаправляющий пользователя на страницу входа.
    """
    logout(request)
    return redirect('login')

def get_results(request: HttpRequest) -> HttpResponse:
    """
    View для страницы терминала.
    Реализована проверка не зарегистрированных пользвателей.
    Основная роль:
        Передает первые данные для отображения их странице с помощью Jinja шаблонов.
        Дальше данные запрашивает AJAX запрос со страницы и его обработает функция update_table из utils.py 
    """
    if request.user.is_authenticated:
        """
        no-prefix - for data from Binance
        prefix [g] - for data from Garantex
        prefix [h] - for data from Huobi
        """
        #binance
        ask = get_binance_rates(type='BUY')
        bid = get_binance_rates(type='SELL')
        
        #garantex
        fiat_lower = 'usd'
        asset_lowet = 'usdt'
        garantex = get_garantex_rates(fiat=fiat_lower, asset=asset_lowet)
        gasks = garantex['asks'][:10]
        gbids = garantex['bids'][:10]

        #huobi
        hbids = get_huobi_rates(type='BUY')
        hasks = get_huobi_rates(type='SELL')
    
        return render(request, 'terminal.html', {'bid': bid, 
                                                 'ask': ask, 
                                                 'gasks':gasks, 
                                                 'gbids':gbids, 
                                                 'hbids':hbids, 
                                                 'hasks':hasks})
    else:
        return HttpResponseForbidden()

def pageNotFound(request: HttpRequest, exception: Exception) -> HttpResponseNotFound:
    """
    Обработчик для страницы с ошибкой 404 (страница не найдена).
    Args:
        request (HttpRequest): Объект запроса.
        exception (Exception): Исключение, вызвавшее ошибку.
    Returns:
        HttpResponseNotFound: HTTP-ответ с сообщением об ошибке 404.
    """
    return HttpResponseNotFound(
        "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;'><style>body {background-color: #000000;color: #eee;}a {color: #FFA500;}</style><title>Oops...</title><h1>Something went wrong</h1><p>Hello! If you want to login to your profile, please go to the login page, which you can find at the following link. There you can enter your username and password to access your profile. If you encounter any issues with logging in, please contact our support team. Thank you!</p><p><a href='/' style='text-align:center;'>Login</a></p></div>"
    )

def terms(request: HttpRequest) -> HttpResponse:
    """
    View для страницы с правилами.
    """
    return render(request, 'termsandco.html')

def contact(request: HttpRequest) -> HttpResponse:
    """
    View для страницы с контактной информацией.
    """
    return render(request, 'contact.html')
