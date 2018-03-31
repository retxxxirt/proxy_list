from .proxy_list import ProxyList

proxy_list = ProxyList()

update = proxy_list.update

start_update = proxy_list.start_update
stop_update = proxy_list.stop_update

get = proxy_list.get
get_all = proxy_list.get_all