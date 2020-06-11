import json
from pygraphml import GraphMLParser
from pygraphml import Graph

NAME_OF_INPUT_FILE = 'results/wikipages.json'
NAME_OF_OUTPUT_FILE = 'results/graph3.graphml'


class Wikipage:
    def __init__(self, url, title, id=None, mainCategory=None):
        self.url = url
        self.title = title
        self.id = id
        self.mainCategory = mainCategory
        self.linksTo = set()

    def addLink(self, linkedPageId):
        if (linkedPageId in self.linksTo):
            # print("Skip link ", linkedPageId, " for page ", self.title)
            return False
        else:
            self.linksTo.add(linkedPageId)
            return True
    
    def __eq__(self, another):
        return hasattr(another, 'url') and self.url == another.url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        return "Page [TITLE=\'" + self.title + "\', URL=" + self.url

def main():
    with open(NAME_OF_INPUT_FILE) as f:
        data = json.load(f)
    wikipages = createWikipages(data)
    print(len(wikipages))
    writeToGraphml(wikipages, NAME_OF_OUTPUT_FILE)

def createWikipages(jsonData):
    categories = createCategories(jsonData)
    pages = []
    urlToId = {}
    # creating all the nodes
    for currentId, currentPage in enumerate(jsonData):
        urlToId[currentPage['url']] = currentId
        mainCategory = getMainCategory(currentPage['categories'], categories)
        page = Wikipage(currentPage['url'], currentPage['title'], id=currentId, mainCategory=mainCategory)
        pages.append(page)
    # creating all the edges
    for currentPage in jsonData:
        currentPageId = urlToId[currentPage['url']]
        if 'links' in currentPage:
            for link in currentPage['links']:
                if link['url'] in urlToId:
                    pages[currentPageId].addLink(urlToId[link['url']])
    return pages

# creating all the categories
def createCategories(jsonData):
    categories = {}
    for page in jsonData:
        for category in page['categories']:
            catObject = Wikipage(category['url'], category['title'])
            if catObject in categories:
                categories[catObject] += 1
            else:
                categories[catObject] = 1
    # categoriesSortedByAppearanceDesc = [key for key, _ in sorted(categories.items(), key=lambda item: item[1], reverse=True)]
    return categories

# get the one category in categoryList, that occurs most inin categories
def getMainCategory(categoryList, categories):
    currentMainCat = None
    appearanceMainCat = 0
    for c in categoryList:
        catObject = Wikipage(c['url'], c['title'])
        if categories[catObject] > appearanceMainCat:
            currentMainCat = catObject
            appearanceMainCat = categories[catObject]
    return currentMainCat


def writeToGraphml(pages, fileName):
    graph = Graph()
    nodes = []
    # creating nodes
    for page in pages:
        node = graph.add_node(page.id)
        node['title'] = page.title
        node['url'] = page.url
        if not page.mainCategory is None:
            node['main_category'] = page.mainCategory.title
        nodes.append(node)
    # creating edges
    for page in pages:
        # if there are edges
        if page.linksTo:
            for pageId in page.linksTo:
                e = graph.add_edge(nodes[page.id], nodes[pageId])
                e.set_directed(True)
    parser = GraphMLParser()
    parser.write(graph, fileName)

main()