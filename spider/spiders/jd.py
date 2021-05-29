# -*- coding: utf-8 -*-
from scrapy.http import Request
from ..items import SpiderItem
import scrapy
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return splash:html()
end
'''


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword={0}&enc=utf-8&page={1}']

    def __init__(self, keyword='', page=1, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.page = int(page) + 1

    def start_requests(self):
        url = self.start_urls[0]
        # url = 'https://item.jd.com/57000824319.html'
        # yield SplashRequest(url, endpoint='execute',
        #                     args={'lua_source': lua_script, 'timeout': 50, 'wait': 0.5}, cache_args=['lua_source'],
        #                     callback=self.img_url_parse)
        for i in range(1, self.page):
            url = url.format(self.keyword, i)
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        goods_url_list = response.xpath('//div[@id="J_goodsList"]/ul/li//div[@class="p-img"]/a/@href').extract()
        for goods_url in goods_url_list:
            yield SplashRequest('https:' + goods_url, endpoint='execute',
                                args={'lua_source': lua_script, 'timeout': 80, 'wait': 0.5}, cache_args=['lua_source'],
                                callback=self.img_url_parse)

    def img_url_parse(self, response):
        style_content = response.xpath('//div[@id="J-detail-content"]/style/text()').extract_first()

        # 实例化item对象
        item = SpiderItem()

        if style_content is None:
            img_list = response.xpath('//div[@id="J-detail-content"]/p/img/@data-lazyload').extract()
            for img in img_list:
                if 'http:' in img or 'https:' in img:
                    item['img_url'] = [img]
                else:
                    item['img_url'] = ['https:' + img]
                yield item
        else:
            img_list = style_content.split('background-image:url(')
            for img in img_list[1:]:
                img_end = img.find(')')
                if 'http:' in img or 'https:' in img:
                    item['img_url'] = [img[0:img_end]]
                else:
                    item['img_url'] = ['https:' + img[0:img_end]]
                yield item
