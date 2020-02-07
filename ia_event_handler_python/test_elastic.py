from elasticsearch5 import Elasticsearch 

# We use elasticsearch5 because we want to send data to a elasticsearch 5.X cluster
# This file is for testing only

# Connection initializer
def createConnection(host, port):
    try:
        esConnection=Elasticsearch([{'host':host ,'port':port}])
        return esConnection
    except Exception as error :
        raise RuntimeError("Error with Elasticsearch connector : " + str(error))


# For testing purpose only
# Add a article to the elasticsearch database
def addArticleToElastic(esIndex,url, ESConnector):
    try:
        article={'url' : url, 'owner' : 'owner', 'sharedBy' : 'lotofpeople', 'tags' : [], 'suggestedTags' : [] }
        ESConnector.create(index=esIndex,id=1,body=article, doc_type='Article')
    except Exception as error :
         raise RuntimeError("Error when creating article in elasticsearch : " + str(error))

url = 'https://www.theguardian.com/global-development/2020/feb/07/coronavirus-chinese-rage-death-whistleblower-doctor-li-wenliang'

connector = createConnection('localhost', '9200')
addArticleToElastic('pocket', url, connector)