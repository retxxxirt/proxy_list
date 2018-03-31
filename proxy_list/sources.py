import requests
from pyquery import PyQuery

def free_proxy_list_net():

    response = requests.get('https://free-proxy-list.net/')

    html, list = PyQuery(response.text), []

    for tr_element in html.find('tbody tr'):

        tr_element = html(tr_element)

        td_elements = tr_element.children('td')

        for i, td_element in enumerate(td_elements):

            td_elements[i] = html(td_element)

        list.append({

            'ip': td_elements[0].text(),
            'port': td_elements[1].text(),

            'type': 'http' if td_elements[6] == 'no' else 'https',

            'country': td_elements[2].text()
        })

    return list

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

    list, tr_elements = [], html.find('.spy1x, .spy1xx')

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

        list.append({

            'ip': td_elements[0].find('.spy14').contents()[0],
            'port': port,

            'type': td_elements[1].text().split('\n')[0].lower(),

            'country': td_elements[4].text().split('\n')[0]
        })

    return list

BUILT_IN_SOURCES = {

    'spys.one': spys_one,
    'free-proxy-list.net': free_proxy_list_net
}

DEFAULT_SOURCES = [key for key in BUILT_IN_SOURCES]