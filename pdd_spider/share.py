from requests_html import HTMLSession


def html_from_uri(uri):
    print('html_from_uri uri: {}'.format(uri))
    try:
        if uri is None:
            return
        session = HTMLSession()
        r = session.get(uri)
        return r.html.html
    except Exception as e:
        print('Exception: {}'.format(e))
        return html_from_uri(uri)


# 把浏览器的cookies字符串转成字典
def cookies2dict(cookies):
    items = cookies.split(';')
    d = {}
    for item in items:
        kv = item.split('=', 1)
        k = kv[0]
        v = kv[1]
        d[k] = v
    return d