import time
import requests
from pyquery import PyQuery

from ..utilities import proxy_is_valid

def free_proxy_list_net():

    def get_data(url):

        response = requests.get(url)

        html, data = PyQuery(response.text), []

        tr_elements = [html(tr_element) for tr_element in html.find('tbody tr')]

        for tr_element in tr_elements:
            data.append([html(td_element).text() for td_element in tr_element.children('td')])

        return data

    proxies, urls = [], [

        'https://free-proxy-list.net',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://free-proxy-list.net/anonymous-proxy.html',
        'https://us-proxy.org',
        'https://sslproxies.org',
        'https://socks-proxy.net'
    ]

    for url in urls:

        for row in get_data(url):

            if url == 'https://socks-proxy.net':

                type = row[4].lower()
                anonymity = row[5].lower()

            else:

                type = 'http' if row[6] == 'no' else 'https'
                anonymity = row[4]

            if anonymity == 'elite proxy':

                anonymity = 'elite'

            proxy = {

                'ip': row[0],
                'port': row[1],

                'type': type,
                'anonymity': anonymity,

                'country': row[2]
            }

            if proxy_is_valid(proxy):

                proxies.append(proxy)

        time.sleep(1)

    return proxies