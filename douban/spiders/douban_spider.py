# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 允许的域名(只在改域名下爬取)
    allowed_domains = ['movie.douban.com']
    # 入口URL,扔到调度器里面
    start_urls = ['http://movie.douban.com/top250']

    # 默认的解析方法
    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        print("-----------------")
        for i_item in movie_list:
            # 导入item文件
            douban_item = DoubanItem()
            # 详细的数据解析
            douban_item['serial_num'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            # 多行数据解析
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[2]/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[@class='quote']/span/text()").extract_first()
            # 将数据yield到管道
            yield douban_item
        # 解析下一页
        next_link = response.xpath("//div[@class='paginator']/span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)