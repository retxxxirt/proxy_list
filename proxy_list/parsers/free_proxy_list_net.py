import time
import requests
from pyquery import PyQuery

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

            else:

                type = 'http' if row[6] == 'no' else 'https'

            proxies.append({

                'ip': row[0],
                'port': row[1],

                'type': type,

                'country': row[2]
            })

        time.sleep(1)

    return proxies