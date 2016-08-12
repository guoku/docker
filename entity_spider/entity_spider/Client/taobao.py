import  time
from entity_spider.Client import BaseClient
from entity_spider.config.job import CRAWL_LINK_INTERVAL

origin_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Referer': 'http://detail.tmall.com/item.htm?id=44691754172'
    }

class TaobaoClient(BaseClient):
    def get_entity_data(self, linkObj):
        resp =  self.get(
                        self.get_request_url(linkObj),
                        headers=self.get_header(),
                        timeout=10
                        )
        time.sleep(CRAWL_LINK_INTERVAL)
        return resp


    def get_request_url(self, linkObj):
        return  linkObj.link

    def get_header(self):
        tmall_header = {
            'Cookie':'thw=cn; cna=ezXlDwoe7FwCAXx/TRpH8og7; v=0; cookie2=1c79f2dce234305569fd56b2d1044b3a; t=252a661e9d3ab099c1b275dcdcfb341c; _tb_token_=f6bf87761ee6e; uc1=cookie14=UoWxNF%2FvBifDVQ%3D%3D; l=ArCw7v/CF2V-dImOEGH7pePjAHAC-ZRD; mt=ci%3D-1_0',
            'User-Agent':'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
         }
        tmall_header.update(origin_headers)
        return tmall_header

    def get_cookie(self):
        return {}


class TaobaoImageClient(BaseClient):
    def get_header(self):
        return {
            'Cookie':'thw=cn; cna=6HD7DxQwdEECAXx/kbO4A0ad; v=0; cookie2=1c7b16667907ebd16a49872c410aa808; t=f98e2a2b3ce20db86edcc2266369b38f; l=AmNjVUoAHRBgEzpHz2B4hqvuc6kNR/ea; isg=Al1daHfT1oiJrLKkDT8PU8_tbD_wLpHMCpe_MB8ihbTj1n0I58qhnCuEZn-p; mt=ci%3D-1_0',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
        }
    pass






