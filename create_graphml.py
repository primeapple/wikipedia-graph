import json
from pygraphml import GraphMLParser
from pygraphml import Graph

NAME_OF_INPUT_FILE = 'article_with_links_and_categories.json'
NAME_OF_OUTPUT_FILE = 'graph.graphml'

with open(NAME_OF_INPUT_FILE) as f:
    data = json.load(f)


class Article:
    def __init__(self, id, title, url, categories):
        self.id = id
        self.title = title
        self.url = url
        self.categories = categories
        self.links_to = []
    
    def __eq__(self, another):
        return hasattr(another, 'url') and self.url == another.url

    def __hash__(self):
        return hash(self.url)

    def add_link(self, linked_article_id):
        self.links_to.append(linked_article_id)

graph = Graph()
graph.directed = False
nodes = []
articles = []
url_to_id = {}
current_id = 0

for a in data:
    url_to_id[a['url']] = current_id
    if 'title' in a:
        a_title = a['title']     
    else: 
        a_title = "unknown title"
        # print("Unknown title for", a['url'])
    if 'categories' in a:
        a_cat = a['categories']     
    else: 
        a_cat = []
        # print("Unknown categories for", a['url'])

    # article = Article(current_id, a_title, a['url'], a_cat)
    # articles.append(article)
    node = graph.add_node(a_title)
    node['url'] = a['url']
    node['categories'] = a_cat
    node['id'] = current_id
    nodes.append(node)
    current_id += 1

for a in data:
    current_article_id = url_to_id[a['url']]
    if 'links' in a:
        for link in a['links']:
            if link['url'] in url_to_id:
                graph.add_edge(nodes[current_article_id], nodes[url_to_id[link['url']]])
                # articles[current_article_id].add_link(url_to_id[link['url']])
    # else:
    #     print("Unknown links for", a['url'])


# with open(NAME_OF_OUTPUT_FILE, "w+") as f:
parser = GraphMLParser()
parser.write(graph, NAME_OF_OUTPUT_FILE)