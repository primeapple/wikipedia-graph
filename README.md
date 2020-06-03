# Wikipedia Graph Project

## About
This project is about visualizing the relationships between Wikipedia Articles according to it's links. So basically want to display Wikipedia articles as a graph, where each article is a node and each link inside the article to another one is an directed edge between these nodes.

We are doing this, without using the Wikipedia Api. Instead we scrap the articles and links inside using [Scrapy](https://scrapy.org/).


## Set Up
First, you have to make sure, to have Docker, Docker-Compose and Python installed.

Then, just follow the steps below:

```bash
# clone the repository
git clone https://github.com/primeapple/wikipedia-graph.git
cd wikipedia-graph
# install scrapyd-deploy
pip install scrapyd-deploy
# starting the docker containers (mongodb, mongodb-express, scrapyd)
docker-compose up
```

Now you can deploy the project to scrapy-d:

```bash
scrapyd-deploy -p wiki
```

This creates a python egg and uploads it to the running scrapyd server.

## Running Spiders
Now we can start the process by running the `articles` spider. This will scrap the url and title of the mathematical articles of Wikipedia. See [this link](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Mathematics/List_of_mathematics_articles_(0%E2%80%939)).
Please choose an appropriate collection name for the mongodb to store the results in.

```bash
curl http://localhost:6800/schedule.json -d project=wiki -d spider=articles -d collection=COLLECTION_NAME
```

Now have a look at [http://localhost:6800/jobs](http://localhost:6800/jobs). There should be a running job. When it finishes, click on the "Items" Link on the job page. This links to an url with a JSON Lines file. Copy this URL!

Now we want to run the `wikipage` spider. Make sure to use another collection name this time:

```bash
curl http://localhost:6800/schedule.json -d project=wiki -d spider=wikipage -d link_start_url_list=LINK_TO_JSON_LINES_FILE -d collection=ANOTHER_COLLECTION_NAME
```

However, this would limit the run to only one thread.

To make it run on multiple threads use the little script I created (of course, use the actual url and an actual number):
```bash
bash ./run_wiki_page_in_scrapyd.sh NUM_OF_THREADS ANOTHER_COLLECTION_NAME LINK_TO_JSON_LINES_FILE
```

## Monitoring
To see the current mongodb state, got to http://localhost:8081/db/wiki/.
To see the current state of scrapy, check out http://localhost:6800/

## Usage without scrapyd
You can also use scrapy without scrapyd. This just makes it harder to run multiple threads (checkout `concurrent_wikipages.py` file, but be aware, that it is not working yet). Please change the `DATABASE_URI` Key in `wiki/settings.py` accordingly.

Install some more dependencies:
```bash
pip install scrapy pymongo
```

To crawl a spider:
```bash
scrapy crawl -a ARGUMENT_KEY=ARGUMENT_VALUE NAME_OF_SPIDER
```

## Visualizing
TODO