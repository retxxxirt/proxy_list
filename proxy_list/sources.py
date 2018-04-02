import json
import requests
from pyquery import PyQuery
from iso3166 import countries

def free_proxy_list_net():

    response = requests.get('https://free-proxy-list.net/')

    html, proxies = PyQuery(response.text), []

    for tr_element in html.find('tbody tr'):

        tr_element = html(tr_element)

        td_elements = tr_element.children('td')

        for i, td_element in enumerate(td_elements):

            td_elements[i] = html(td_element)

        proxies.append({

            'ip': td_elements[0].text(),
            'port': td_elements[1].text(),

            'type': 'http' if td_elements[6].text() == 'no' else 'https',

            'country': td_elements[2].text()
        })

    return proxies

def spys_one():

    response = requests.get('http://spys.one/proxies/')

    html = PyQuery(response.text)

    response = requests.post(

        'http://spys.one/proxies/',

        data = {

            'xpp': 5,
            'xf0': html.find('[name = \'xf0\']').val()
        }
    )

    html = PyQuery(response.text)

    proxies, tr_elements = [], html.find('.spy1x, .spy1xx')

    values, values_source = {}, html(html.find('body script')[2]).text().split(';')

    for value in values_source[:-1]:

        value = value.split('=')

        value[1] = value[1].split('^')

        if len(value[1]) == 1:

            values[value[0]] = int(value[1][0])

        else:

            values[value[0]] = int(value[1][0]) ^ values[value[1][1]]

    for tr_element in tr_elements[1:]:

        td_elements = html(tr_element).find('td')

        for i, td_element in enumerate(td_elements):

            td_elements[i] = html(td_element)

        port, keys = '', td_elements[0].find('.spy14 script').text()[44:-1].replace('(', '').replace(')', '').split('+')

        for key in keys:

            key = key.split('^')

            port += str(values[key[0]] ^ values[key[1]])

        type = td_elements[1].text().split('\n')

        if len(type) > 1 and type[1] == 'S':

            type = ['https']

        proxies.append({

            'ip': td_elements[0].find('.spy14').contents()[0],
            'port': port,

            'type': type[0].lower(),

            'country': td_elements[4].text().split('\n')[0]
        })

    return proxies

def hidester_com():

    response = requests.get(

        'https://hidester.com/proxydata/php/data.php',

        headers = {

            'Host': 'hidester.com',
            'Referer': 'https://hidester.com/proxylist/'
        },

        params = {

            'limit': 100000,
            'mykey': 'data',
            'offset': 0,
            'orderBy': 'latest_check',
            'sortOrder': 'DESC',
        }
    )

    proxies, proxies_source = [], json.loads(response.text)

    for proxy in proxies_source:

        countries_iso3166 = {

            'VENEZUELA': 'Venezuela, Bolivarian Republic of',
            'CURACAO': 'Curaçao',
            'KOREA': 'Korea, Republic of',
            'MOLDOVA': 'Moldova, Republic of',
            'PALESTINIAN TERRITORY': 'Palestine, State of',
            'UNITED KINGDOM': 'United Kingdom of Great Britain and Northern Ireland',
            'VIETNAM': 'Viet Nam',
            'CZECH REPUBLIC': 'Czechia',
            'IRAN': 'Iran, Islamic Republic of',
            'BOLIVIA': 'Bolivia, Plurinational State of'
        }

        for country in countries_iso3166:

            if proxy['country'] == country:

                proxy['country'] = countries_iso3166[country]

        proxies.append({

            'ip': proxy['IP'],
            'port': str(proxy['PORT']),

            'type': proxy['type'],

            'country': countries.get(proxy['country']).alpha2
        })

    return proxies

BUILT_IN_SOURCES = {

    'spys.one': spys_one,
    'free-proxy-list.net': free_proxy_list_net,
    'hidester.com': hidester_com
}

DEFAULT_SOURCES = [key for key in BUILT_IN_SOURCES]