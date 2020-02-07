from elasticsearch5 import Elasticsearch 

def createConnection(host, port, logger):
    try:
        esConnection=Elasticsearch([{'host':host ,'port':port}])
        return esConnection
    except Exception as error :
        logger.critical("Error with Elasticsearch connector : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector : " + str(error))

# Update
def updateSuggestedTags(esIndex,article_url, predicted_tag, ESConnector, logger):
    try:

        doc = {'doc': {'suggestedTags': [str(predicted_tag)]}}
        # This query is for elasticsearch 5.6 !
        res = ESConnector.search(index=esIndex,body={'query':{'match_all':{}},
            "_source": ["url", article_url]}, doc_type='Article')
        logger.debug(str(res))
        articleFoundID = 1

        ESConnector.update(index=esIndex,id=articleFoundID, body=doc, doc_type='Article')


    except Exception as error:
        logger.critical("Error with Elasticsearch connector when trying to update an article : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector when trying to update an article  : " + str(error))
    


# For testing purpose only
# Add a article to the elasticsearch database
def addArticleToElastic(esIndex,url, ESConnector, logger):
    try:
        article={'url' : url, 'owner' : 'owner', 'sharedBy' : 'lotofpeople', 'tags' : [], 'suggestedTags' : [] }
        ESConnector.create(index=esIndex,id=1,body=article, doc_type='Article')
    except Exception as error :
        logger.critical("Error when creating article in elasticsearch : " + str(error))
    