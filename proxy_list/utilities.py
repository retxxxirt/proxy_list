def url_to_parser_name(url):

    return url.split('//')[1].replace('.', '_').replace('-', '_').replace('/', '_')