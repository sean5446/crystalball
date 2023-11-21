
import requests
import re
import json


class Stock:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_cookie_crumb(self):
        self.cookie = self.get_cookie()
        self.crumb = self.get_crumb()
        return self.cookie, self.crumb

    def get_cookie(self):
        response = self.session.get(
            url='https://fc.yahoo.com', 
            headers=self.headers,
            allow_redirects=True
        )
        cookie = str(list(response.cookies)[0])
        pattern = 'Cookie ([A-Za-z0-9]+)=(\S+) '
        match = re.search(pattern, cookie)
        if match:
            self.cookie = {match.group(1): match.group(2) }
            return self.cookie
        return None

    def get_crumb(self) -> str:
        response = self.session.get(
            url='https://query1.finance.yahoo.com/v1/test/getcrumb',
            headers=self.headers,
            cookies=self.cookie,
            proxies=None, 
            timeout=30, 
            allow_redirects=True,
        )
        self.crumb = response.content.decode('UTF-8')
        return self.crumb

    def get_quote(self, symbol):
        params = {
            'modules': 'financialData,quoteType,defaultKeyStatistics,assetProfile,summaryDetail', 
            'ssl': 'true',
            'crumb': self.crumb,
        }
        response = self.session.get(
            url=f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}", 
            headers=self.headers, 
            params=params, 
            timeout=30,
        )
        return json.loads(response.content.decode('UTF-8'))

    def is_symbol_up(self, symbol):
        info = self.get_quote(symbol)
        details = info['quoteSummary']['result'][0]['summaryDetail']
        close = float(details['previousClose']['raw'])
        bid = float(details['bid']['raw'])
        if bid - close >= 0:
            return True, close, bid
        else:
            return False, close, bid
