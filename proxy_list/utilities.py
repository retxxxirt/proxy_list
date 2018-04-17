import re

def validate_proxy(proxy):

    assert 'ip' and 'port' and 'type' and 'anonymity' and 'country' in proxy

    assert re.match('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', proxy['ip'])

    assert re.match('^[0-9]{1,5}$', proxy['port'])

    assert proxy['type'] in ['http', 'https', 'socks4', 'socks5']

    assert proxy['anonymity'] in ['transparent', 'anonymous', 'elite']

    assert re.match('^[A-Z]{2}$', proxy['country'])

def proxy_is_valid(proxy):

    try:

        validate_proxy(proxy)

        return True

    except:

        return False

def validate_selector(proxy, selector):

    for key in selector:

        if type(selector[key]) != list:

            selector[key] = [selector[key]]

    for key in selector:

        assert proxy[key] in selector[key]

def selector_is_valid(proxy, selector):

    try:

        validate_selector(proxy, selector)

        return True

    except:

        return False