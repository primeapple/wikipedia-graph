import scrapy
from ..items import WikipageItem, WikipageLoader

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Mathematics/List_of_mathematics_articles_(0%E2%80%939)'
    ]

    def __init__(self, start_urls=None, collection=None, *args, **kwargs):
        super(ArticlesSpider, self).__init__(*args, **kwargs)
        self.collection = collection


    def parse(self, response):
        for article in response.xpath("//div[@class='mw-parser-output']/p/a"):
            # there are some hidden links, we don't want them
            if article.xpath("./text()").get() != " ":
                loader = WikipageLoader(item=WikipageItem(), response=response)
                loader.add_value('title', article.xpath("./text()").get())
                loader.add_value('url', response.urljoin(article.xpath("./@href").get()))
                yield loader.load_item()

        current_page = response.xpath("//div[@class='mw-parser-output']/table/tbody/tr[3]/td/a[@class='mw-selflink selflink']")
        next_page = current_page.xpath("./following-sibling::a")
        # add next page, if there is one (0-9, A, B, ..., Z)
        if next_page:
            url = response.urljoin(next_page.xpath("@href").get())
            yield scrapy.Request(url, callback = self.parse)