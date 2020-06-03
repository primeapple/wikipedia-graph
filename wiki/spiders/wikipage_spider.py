import scrapy
import json
import requests
from ..items import WikipageItem, WikipageLoader

    
def get_start_urls(start_urls, link, parts, this_part):
    urls = []
    # if spider was called from commandline or program
    if start_urls is not None:
        # called from commandline
        if isinstance(start_urls, str):
            # if start_urls is in list form
            if start_urls.startswith('['):
                urls = start_urls[1:-1].split(',')
        # if spider was called from another program
        elif isinstance(start_urls, list):
            urls = start_urls
    # link is not none
    elif link is not None:
        response = requests.get(link)
        # convert jsonlines file
        json_data = [json.loads(line) for line in response.text.split('\n')[:-1]]
        urls = [item['url'] for item in json_data]
    return urls[this_part::parts]


class WikipageSpider(scrapy.Spider):
    name = "wikipage"
    start_urls = []

    def __init__(self, start_urls=None,
            link_start_url_list=None,
            file_start_url_list=None,
            parts_to_divide_into=1,
            this_part_number=0,
            collection=None,
            *args, **kwargs):

        super(WikipageSpider, self).__init__(*args, **kwargs)
        self.start_urls = get_start_urls(
            start_urls,
            link_start_url_list, 
            int(parts_to_divide_into), 
            int(this_part_number))
        self.collection = collection


    def parse(self, response):
        # some metadata about the current page
        wikipageLoader = WikipageLoader(item=WikipageItem(), response=response)
        wikipageLoader.add_xpath('title', "//h1[@class='firstHeading']//text()")
        wikipageLoader.add_value('url', response.url)

        # handle categories at the bottom of the wikipage
        categories = []
        for category in response.xpath("//div[@id='catlinks']/div[@class='mw-normal-catlinks']/ul/li/a"):
            url = response.urljoin(category.xpath(".//@href").get())
            categoryLoader = WikipageLoader(item=WikipageItem(), response=response)
            categoryLoader.add_value('title', category.xpath("./text()").get())
            categoryLoader.add_value('url', url)
            categories.append(categoryLoader.load_item())
        wikipageLoader.add_value('categories', categories)

        # handle links in the wikipage
        links = []
        for link in response.xpath("//div[@class='mw-parser-output']/p/a"):
            url = response.urljoin(link.xpath(".//@href").get())
            # only look for links inside wikipedia
            if (url.startswith("https://en.wikipedia.org/wiki/")):
                linkLoader = WikipageLoader(item=WikipageItem(), response=response)
                linkLoader.add_value('title', link.xpath("./@title").get())
                linkLoader.add_value('url', url)
                links.append(linkLoader.load_item())
        wikipageLoader.add_value('links', links)
        return wikipageLoader.load_item()

