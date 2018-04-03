import js2py
import requests
from pyquery import PyQuery
from functools import partial

from proxy_list.utilities import url_to_parser_name

group = 'spys.one'

def get_proxies(url):

    response = requests.post(url, data = {

        'xpp': 5
    })

    html = PyQuery(response.text)

    js_secret_code = html(html.find('body script')[2]).text()

    proxies, tr_elements = [], [html(tr_element) for tr_element in html.find('.spy1x, .spy1xx')]

    for tr_element in tr_elements[1:]:

        td_elements = [html(td_element) for td_element in tr_element.children('td')]

        type = td_elements[1].text().split('\n')

        if len(type) > 1 and type[1] == 'S':

            type = ['https']

        js_port_code = '; function a() {return \'\'%s} a()' % td_elements[0].find('.spy14 script').text()[43:-1]

        proxies.append({

            'ip': td_elements[0].find('.spy14').contents()[0],
            'port': str(js2py.eval_js(js_secret_code + js_port_code)),

            'type': type[0].lower(),

            'country': td_elements[3].children('a').attr('href').split('/')[-2]
        })

    return proxies

parsers, urls = [], [

    'http://spys.one/en/free-proxy-list/',
    'http://spys.one/en/anonymous-proxy-list/',
    'http://spys.one/en/https-ssl-proxy/',
    'http://spys.one/en/socks-proxy-list/',
    'http://spys.one/en/http-proxy-list/'
]

for url in urls:

    def parse(url):

        return get_proxies(url)

    parser = partial(parse, url)

    parser.__name__ = url_to_parser_name(url)

    parsers.append(parser)