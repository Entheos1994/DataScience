# -*- coding: utf-8 -*-
import scrapy

from bbc.items import Recipe

class RecipeSpider(scrapy.Spider):
    name = "recipes"
    allowed_domains = ["bbc.co.uk"]

    # Search for healthy recipes using the 'healthy' keyword, start form page 1
    start_urls = (
        'http://www.bbc.co.uk/food/chefs/by/letters/q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m',
    )

    def parse(self, response):
        # Get the list of chefs in the current page
        chefs = response.xpath('//*[(@id = "chefs-by-letter")]//a/@href').extract()
        # From each recipe extract the name and url
        for chef in chefs:
            chef_page = response.urljoin(chef)
            print chef_page
            yield scrapy.Request(chef_page, callback=self.parseChef)

    def parseChef(self, response):
        # Extract recipes of the current chef
        recipes = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "resources", " " ))]//a')
        for recipe in recipes:
            item = Recipe()
            # the text field could be a list -> join
            # and could contain an insane amount of spaces and tabs -> strip
            name = ''.join(recipe.xpath('text()').extract()).strip('\r\n \t')
            item['name'] = name
            item['url'] = 'http://www.bbc.co.uk' + recipe.xpath('@href').extract()[0]
            yield item
