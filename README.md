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
# install scrapyd-client
pip install git+https://github.com/scrapy/scrapyd-client
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
scrapyd-client schedule -p wiki --arg collection=articles_new articles
```

Now have a look at [http://localhost:6800/jobs](http://localhost:6800/jobs). There should be a running job. When it finishes, click on the "Items" Link on the job page. This links to an url with a JSON Lines file. Copy this URL!

We COULD use the same way to run the `wikipage` spider. Use another collection name this time.  
However, this would limit the run to only one thread.

```bash
scrapyd-client schedule -p wiki --arg link_start_url_list=LINK_TO_JSON_LINES_FILE --arg collection=ANOTHER_COLLECTION_NAME wikipage
```

The better way, to make it run on multiple threads use the little script I created (of course use the fitting arguments):

```bash
bash ./run_wiki_page_in_scrapyd.sh NUM_OF_THREADS COLLECTION_NAME LINK_TO_JSON_LINES_FILE
```

## Monitoring
To see the current mongodb state, got to http://localhost:8081/db/wiki/.
To see the current state of scrapy, check out http://localhost:6800/

## Usage without scrapyd
You can also use scrapy without scrapyd. This just makes it harder to run multiple threads (checkout `concurrent_wikipages.py` file, but be aware, that it is not working yet). Please change the `DATABASE_URI` Key in `wiki/settings.py` accordingly.

Install some more dependencies:
```bash
pip install pymongo
```

To crawl a spider:
```bash
scrapy crawl -a ARGUMENT_KEY=ARGUMENT_VALUE NAME_OF_SPIDER
```

## Visualizing
We use [Gephi](https://gephi.org/) to visualize the results, so be sure to download this. However you can use any software that you want.

### Creating a Graph File
First of all we need to create a graph file. We decided to use [GraphML](https://en.wikipedia.org/wiki/GraphML) for this. So first we need to install a graphml parser for python:
```bash
pip install pygraphml
```
After this, please download the json file of the result from the `wikipage` spider from the mongodb, that we set up before. It is recommend to place it in the `results/` folder.  
Now lets look into the `create_graphml.py` file. Here you have to set the input and output filename (line 5-6). The input file is the path to your wikipage json result. The output file is the path where you want to output your `.graphml` file to.

Now run the python script:
```bash
python create_graphml.py
```

### Using Gephi
You can now load your file into Gephi. Make sure to check that the edges are set as directed (should be so by default).

In the overview tab you will now see a black square. This is the graph, but we need to make sure it looks a little better. To do this, use the `OpenOrd` Algorithm below `Layout` (you may also use another algorithm but this one is the fastest). After running the algorithm, check `Appearance` -> `Nodes` -> `partition` -> `main_category` as attribute. Here you can also add more colors.

Feel free to visualize the graph even more. Write us some issues or feedback. Tell us what you found. Add some nice pictures!

Enjoy!