import requests
from pyquery import PyQuery
from functools import partial

from proxy_list.utilities import url_to_parser_name

group = 'free-proxy-list.net'

def parse_data(url):

    response = requests.get(url)

    html, data = PyQuery(response.text), []

    tr_elements = [html(tr_element) for tr_element in html.find('tbody tr')]

    for tr_element in tr_elements:

        data.append([html(td_element).text() for td_element in tr_element.children('td')])

    return data

def socks_proxy_net():

    data, proxies = parse_data('https://socks-proxy.net'), []

    for row in data:

        proxies.append({

            'ip': row[0],
            'port': row[1],

            'type': row[4].lower(),

            'country': row[2]
        })

    return proxies

parsers = [socks_proxy_net]

urls = [

    'https://free-proxy-list.net',
    'https://free-proxy-list.net/uk-proxy.html',
    'https://free-proxy-list.net/anonymous-proxy.html',
    'https://us-proxy.org',
    'https://sslproxies.org'
]

for url in urls:

    def parse(url):

        data, proxies = parse_data(url), []

        for row in data:

            proxies.append({

                'ip': row[0],
                'port': row[1],

                'type': 'http' if row[6] == 'no' else 'https',

                'country': row[2]
            })

        return proxies

    parser = partial(parse, url)

    parser.__name__ = url_to_parser_name(url)

    parsers.append(parser)