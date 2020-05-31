import json
from scrapy.crawler import CrawlerProcess
from wiki.spiders.wikipage_spider import WikipageSpider
from scrapy.utils.project import get_project_settings
from wiki import settings
from datetime import datetime
import multiprocessing 
# setting the number of spiders to run concurrently
NUM_WIKIPAGE_SPIDERS = 2

# importing the settings
settings = get_project_settings()
settings.set('COLLECTION_NAME', datetime.now().strftime('date_%Y_%m_%d_%H_%M_%S'))
# reading the data
with open('final_articles.json') as f:
    json_data = json.load(f)
    urls = [page['url'] for page in json_data]
urls = urls[:500]
splitted_urls = [urls[i::NUM_WIKIPAGE_SPIDERS] for i in range(0, NUM_WIKIPAGE_SPIDERS)]

processes = []
# running the processes in parallel
for i in range(0, NUM_WIKIPAGE_SPIDERS):
    crawler = CrawlerProcess(settings=settings)
    crawler.crawl(WikipageSpider, start_urls=splitted_urls[i])
    p = multiprocessing.Process(target=crawler.start)
    processes.append(p)
    p.start()
    print("Starting process", i)

# waiting for the processes to finish
for process in processes:
    process.join()