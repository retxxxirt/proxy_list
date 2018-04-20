from distutils.core import setup

setup(

    name = 'proxy_list',
    packages = ['proxy_list'],
    version = '0.3.6',
    description = 'Free proxy lists',
    author = 'retxxxirt',
    author_email = 'retxxirt@gmail.com',
    url = 'https://github.com/retxxxirt/proxy_list',
    keywords = ['proxy', 'proxies', 'proxy list', 'free', 'free proxy', 'free proxies'],
    install_requires = ['requests[socks]', 'pyquery', 'iso3166', 'js2py'],
    package_data = {'proxy_list': ['parsers/*.py']}
)