from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse


# Create your views here.

def home_view(request):
    # Fetch cryptocurrency market data from the CoinGecko API
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'

    # Fetch and parse the cryptocurrency market data
    data = requests.get(url).json()

    # Fetch cryptocurrency news data from the CryptoCompare API
    newses = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN").json()

    # Function to format market capitalization values
    def format_market_cap(market_cap):
        if market_cap >= 1_000_000_000:
            return "{:,.2f}B".format(market_cap / 1_000_000_000)
        elif market_cap >= 1_000_000:
            return "{:,.2f}M".format(market_cap / 1_000_000)
        else:
            return "{:,.2f}".format(market_cap)

    # Loop through the cryptocurrency data and format market capitalization values
    for item in data:
        if 'market_cap' in item and isinstance(item['market_cap'], (int, float)):
            item['market_cap'] = format_market_cap(item['market_cap'])

    # Context dictionary containing the cryptocurrency data and news data
    context = {
        'data': data,  # Cryptocurrency market data
        'newses': newses['Data']  # Cryptocurrency news data
    }

    # Render the main HTML template with the context data
    return render(request, 'positions/main.html', context)
