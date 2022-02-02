
import requests
import json
from tokens import API_KEY

class APIException(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class MyBot:
    def __init__(self) -> None:
        self.html_curr = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={API_KEY}').content
        self.curr_dict = json.loads(self.html_curr)['results']

    @staticmethod
    def get_price(base, quote, amount):
        html_curr = requests.get(f'https://free.currconv.com/api/v7/convert?q={base}_{quote},{quote}_{base}&compact=ultra&apiKey={API_KEY}').content
        _curr = json.loads(html_curr)
        rez = round(_curr[base+'_'+quote]*amount, 2)
        return f'{amount} {base} это {rez} {quote}'  
