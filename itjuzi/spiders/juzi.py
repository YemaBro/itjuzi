# -*- coding: utf-8 -*-
import scrapy
import json
from itjuzi.items import ItjuziItem


class JuziSpider(scrapy.Spider):
    name = 'juzi'
    allowed_domains = ['itjuzi.com']

    def start_requests(self):
        url = 'https://www.itjuzi.com/api/authorizations'
        params = {'account': '18186473835',
                  'password': '147896325'}
        yield scrapy.Request(url=url,
                             method='POST',
                             body=json.dumps(params),
                             headers={'Content-Type': 'application/json'},
                             callback=self.parse)

    def parse(self, response):
        login_msg = json.loads(response.text)
        token = login_msg.get('data').get('token')
        invest_url = 'https://www.itjuzi.com/api/investevents'
        headers = {
            # 'Cookie': 'juzi_token',
            'Authorization': token,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.itjuzi.com/investevent',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Connection': 'keep-alive',
            'Origin': 'https://www.itjuzi.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'CURLOPT_FOLLOWLOCATION': 'true',
        }
        params = {"pagetotal": 0, "total": 0, "per_page": 20,
                  "page": 1, "type": 1, "scope": "", "sub_scope": "",
                  "round": [], "valuation": [], "valuations": "",
                  "ipo_platform": "", "equity_ratio": "",
                  "status": "", "prov": "", "city": [],
                  "time": [], "selected": "", "location": "",
                  "currency": [], "keyword": ""}
        yield scrapy.Request(url=invest_url,
                             method='POST',
                             body=json.dumps(params),
                             headers=headers,
                             cookies={'Cookie': 'juzi_token'},
                             meta={'headers': headers},
                             callback=self.parse_info
                             )

    def parse_info(self, response):
        # token = response.meta['token']
        total = json.loads(response.text).get('data').get('page').get('total')
        headers = response.meta['headers']
        invest_url = 'https://www.itjuzi.com/api/investevents'
        if type(total/20) is not int:
            page_total = total//20 + 1
        else:
            page_total = total//20

        for i in range(1, page_total+1):
            params = {"pagetotal": 0, "total": 0, "per_page": 20,
                      "page": i, "type": 1, "scope": "", "sub_scope": "",
                      "round": [], "valuation": [], "valuations": "",
                      "ipo_platform": "", "equity_ratio": "",
                      "status": "", "prov": "", "city": [],
                      "time": [], "selected": "", "location": "",
                      "currency": [], "keyword": ""}
            yield scrapy.Request(url=invest_url,
                                 method='POST',
                                 body=json.dumps(params),
                                 headers=headers,
                                 cookies={'Cookie': 'juzi_token'},
                                 callback=self.parse_detail
                                 )

    def parse_detail(self, response):
        msg = json.loads(response.text).get('data').get('data')
        for i in msg:
            item = ItjuziItem()
            item['name'] = i.get('name')
            item['com_scope'] = i.get('com_scope')
            item['round'] = i.get('round')
            item['money'] = i.get('money')
            item['investor'] = [k.get('name') + '/' + k.get('type') for k in i.get('investor')]
            item['valuation'] = str(i.get('valuation')) + '万人民币'
            item['prov'] = i.get('prov') + '/' + i.get('city')
            item['agg_time'] = i.get('agg_time')
            item['com_registered_name'] = i.get('com_registered_name')
            yield item


