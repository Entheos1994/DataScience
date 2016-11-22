# -*- coding: utf-8 -*-
import scrapy, pymongo
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bbc.items import Recipe

class IngredientsSpider(CrawlSpider):
    name = 'ingredients'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['http://www.bbc.co.uk/food/ingredients/by/letter/a']
    rules = [ Rule(LinkExtractor(allow=r'[a-z]$'), callback='parse_item', follow=False) ]
    seen = set()


    def parse_item(self, response):
        ingredients = response.css('#foods-by-letter a:nth-child(1)')
        for ingredient in ingredients:
            ingredient_page = ingredient.css('a::attr(href)').extract()[0]
            new_url = response.urljoin(ingredient_page)
            yield scrapy.Request(new_url, callback=self.parse_ingredient)


    def parse_ingredient(self, response):
        recipes = response.css('.resources a')
        for recipe in recipes:
            item = Recipe()
            url = recipe.css('a::attr(href)').extract()[0]
            name = ''.join(recipe.xpath('text()').extract()).strip()
            if not url in self.seen:
                item['name'] = name
                item['url'] = response.urljoin(url)
                print len(self.seen)
                self.seen.add(url)
                yield item



