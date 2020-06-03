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

Now you have the basic setup. Next we want to actually run a spider and save the results in the mongodb. To do this, first choose a collection name and change the `COLLECTION_NAME` key in the `wiki/settings.py` file accordingly.

Now you can deploy the project to scrapy-d:

```bash
scrapyd-deploy -p wiki
```

This creates a python egg and uploads it to the running scrapyd server.

## Running Spiders
Now we can start the process by running the `articles` spider. This will scrap the url and title of the mathematical articles of Wikipedia. See [this link](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Mathematics/List_of_mathematics_articles_(0%E2%80%939)).
Run:
```bash
curl http://localhost:6800/schedule.json -d project=wiki -d spider=articles
```

Now have a look at [http://localhost:6800/jobs](http://localhost:6800/jobs). There should be a running job. When it finishes, click on the "Items" Link on the job page. This links to an url with a JSON Lines file. Copy this URL!

Change you `COLLECTION_NAME` in the `wiki/settings.py` file again. In this next collection, we will store the actual contents of the articles, that we scraped.  
Deploy your project to scrapyd again, to make scrapyd recognize the changes.

Now we want to run the `wikipage` spider. You could run:

```bash
curl http://localhost:6800/schedule.json -d project=wiki -d spider=wikipage -d link_start_url_list=LINK_TO_JSON_LINES_FILE
```

However, this would limit the run to only one thread.

To make it run on multiple threads use the little script I created (of course, use the actual url and an actual number):
```bash
bash ./run_wiki_page_in_scrapyd.sh NUM_OF_THREADS LINK_TO_JSON_LINES_FILE
```

## Visualizing
TODO

## Monitoring

To see the current mongodb state, got to http://localhost:8081/db/wiki/.
To see the current state of scrapy, check out http://localhost:6800/
