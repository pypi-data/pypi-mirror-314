from base.client import *

if __name__=="__main__":
    login('keta', 'http://keta-web.keta-nightly.ketaops.cc', 'eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eJxFjE0KQiEUhbcSd6zgT2q6m_tSwZKI1EcQraBx62jUlqJldIvgncGB7-NwLrDrBQJ4kdAo7bgX0fK1s5lPFB6VF5LKGERgUFqj8T71L7QxLYAj_mFby-r1vL0fd9LpfIQgndR244XSDA5T_gkCLaSnS-yLUJbBXE59YIWQsbZ0_QDRSy8g.EoM4_6RXdOLOmjyZbdnZy0otRX0r_DTtaCaS7-jnUafB5Zqt4ohoi0cvXNpFXvpZIOjqAYUyNO7DTzXV7TXbag')

    path = 'repos'
    query_params = {}  # 这是示例查询参数
    custom_headers = {}  # 这是示例自定义头

    response = request_get(path, query_params, custom_headers)
    if response:
        print(response.status_code)
        print(response.json())
    else:
        print("Failed to send request.", response, response.json())