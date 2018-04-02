This package help you to manage proxy list.

Recently support next sites:
<a href = 'http://spys.one/proxies/'>spys.one</a>,
<a href = 'https://free-proxy-list.net/'>free-proxy-list.net</a>,
<a href = 'https://hidester.com/proxylist/'>hidester.com</a>
and your custom parsers.

<h2> Installation </h2>

    pip install proxy_list

<h2> Usage </h2>

```python
import proxy_list
import requests

proxy_list.update()

proxy = proxy_list.get({'counrty': ['US', 'GB'], 'type': 'https'})

response = request.get('https://google.com', proxy = {'https': proxy['address'])})
```

<h2> Methods </h2>

<h3> update </h3>

Update proxy list.

<h4> Arguments: </h4>
<ul>
    <li>
        <b>sources</b>
        - list of sources. May contain name of built-in parser
        (for example 'spys.one') or custom parser definitions. This definition
        should return list of proxy objects. Default - all built-in parsers.
    </li>
    <li>
        <b>check</b>
        - False, if you doesn't want check proxy. May be True or parameters dict.
        Dict may contain timeout (default 10s) and chunk_size (default 100).
        chunk_size - number of proxies, which are checked together.
    </li>
</ul>

<h3> start_update </h3>

Start update proxy list with interval.

<h4> Arguments: </h4>
<ul>
    <li> <b>interval</b> - interval of update. Default - 300s</li>
    <li>
        <b>sources</b>
        - list of sources. May contain name of built-in parser
        (for example 'spys.one') or custom parser definitions. This definition
        should return list of proxy objects. Default - all built-in parsers.
    </li>
    <li>
        <b>check</b>
        - False, if you doesn't want check proxy. May be True or parameters dict.
        Dict may contain timeout (default 10s) and chunk_size (default 100).
        chunk_size - number of proxies, which are checked together.
    </li>
</ul>

<h3> stop_update </h3>

Stop update proxy list.

<h3> get </h3>

Return a random proxy object.

    'ip': '***.***.***.***',
    'port': '****',
    'address': '****://***.***.***.***:****',
    'type': '****', # http, htpps, socks4, socks5
    'country': '**' # counrty code, for example: US, GB, RU

<h4> Arguments: </h4>
<ul>
    <li>
        <b>selector</b>
        - selector by proxy object parameters. May contain one value for parameter or
        list of values. For example:
    </li>

    {'country': 'US', 'port': ['80', '8080']}
</ul>

<h3> get_all </h3>

Return proxy list.

<h4> Arguments: </h4>
<ul>
    <li>
        <b>selector</b>
        - selector by proxy object parameters. May contain one value for parameter or
        list of values.
    </li>
</ul>
