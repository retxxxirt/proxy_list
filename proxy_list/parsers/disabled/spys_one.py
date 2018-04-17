import time
import js2py
import requests
from pyquery import PyQuery

from proxy_list.utilities import proxy_is_valid

def spys_one():

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

                type = 'https'

            else:

                type = type[0].lower()

            js_port_code = '; function a() {return \'\'%s} a()' % td_elements[0].find('.spy14 script').text()[43:-1]

            port = str(js2py.eval_js(js_secret_code + js_port_code))

            anonymity_dict = {

                'NOA': 'transparent',
                'ANM': 'anonymous',
                'HIA': 'elite'
            }

            proxy = {

                'ip': td_elements[0].find('.spy14').contents()[0],
                'port': port,

                'type': type,
                'anonymity': anonymity_dict[td_elements[2].text()],

                'country': td_elements[3].children('a').attr('href').split('/')[-2]
            }

            if proxy_is_valid(proxy):

                proxies.append(proxy)

        return proxies

    proxies, urls = [], [

        'http://spys.one/en/free-proxy-list/',
        'http://spys.one/en/anonymous-proxy-list/',
        'http://spys.one/en/https-ssl-proxy/',
        'http://spys.one/en/socks-proxy-list/',
        'http://spys.one/en/http-proxy-list/'
    ]

    for url in urls:

        proxies += get_proxies(url)

        time.sleep(1)

    return proxies