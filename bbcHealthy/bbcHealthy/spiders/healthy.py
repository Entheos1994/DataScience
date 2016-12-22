# -*- coding: utf-8 -*-
import scrapy
import os
from bbcHealthy.items import Recipe

class HealthySpider(scrapy.Spider):
    name = "healthy"
    allowed_domains = ["bbc.co.uk"]
    seen = set()
    # generate list from the mongodb of the urls already visited
    os.system('mongo --quiet --eval "db.bbchealthy.distinct("url")" recipes > bbchealthyurls.txt')
    with open('bbchealthyurls.txt') as f:
        seen_urls = f.readlines()
        seen_urls = map(str.strip,seen_urls)
    for el in seen_urls:
        cleand_url = el.strip('\",')
        seen.add(cleand_url)

    # Search for healthy recipes using the 'healthy' keyword, start form page 1
    start_urls = (
        'http://www.bbc.co.uk/food/recipes/search?page=1&diets%5B0%5D=healthy&sortBy=lastModified',
    )

    def parse(self, response):
        # Get the list of links to recipes in the current page
        recipes = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "left", " " ))]//a')
        # From each recipe extract the name and url
        for recipe in recipes:
            item = Recipe()
            item['name'] = recipe.xpath('text()').extract()[0]
            item['url'] = 'http://www.bbc.co.uk' + recipe.xpath('@href').extract()[0]
            if not item['url'] in self.seen:
                self.seen.add(item['url'])
                print(len(self.seen))
                # yield item
        # Search for a next in the page
        next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagInfo-page-numbers-next", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "see-all-search", " " ))]/@href').extract_first()
        # If there is a next parse recursively
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
