from django.shortcuts import render
import requests
from django.http import HttpResponse


# Create your views here.

def home_view(request):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()

    # Grab Crypto News Data
    newses = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN").json()

    # for item in data:
    #     item['market_cap'] = "{:,.0f}".format(item['market_cap'])

    def format_market_cap(market_cap):
        if market_cap >= 1_000_000_000:
            return "{:,.2f}B".format(market_cap / 1_000_000_000)
        elif market_cap >= 1_000_000:
            return "{:,.2f}M".format(market_cap / 1_000_000)
        else:
            return "{:,.2f}".format(market_cap)

    search_term = request.GET.get('search')
    if search_term:
        search_term = search_term.lower()
        data = [item for item in data if 'name' in item and search_term in item['name'].lower()]
    for item in data:
        if 'market_cap' in item and isinstance(item['market_cap'], (int, float)):
            item['market_cap'] = format_market_cap(item['market_cap'])

    context = {
        'data': data,
        'newses': newses['Data']
    }

    return render(request, 'positions/main.html', context)


def prices(request):
    notfound = False
    if request.method == 'POST':
        quote = request.POST.get('quote').upper()
        prices = requests.get(
            "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD").json()
        return render(request, 'crypto_proj/prices.html', {'quote': quote, 'prices': prices})
    else:
        notfound = True
    return render(request, 'crypto_proj/prices.html', {'notfound': notfound})
