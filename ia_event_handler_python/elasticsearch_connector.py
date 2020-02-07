from elasticsearch5 import Elasticsearch 

# We use elasticsearch5 because we want to send data to a elasticsearch 5.X cluster

# Connection initializer
def createConnection(host, port, logger):
    try:
        esConnection=Elasticsearch([{'host':host ,'port':port}])
        return esConnection
    except Exception as error :
        logger.critical("Error with Elasticsearch connector : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector : " + str(error))

# Update the article suggestedTags
# article_url is unique so we only need to find the id of the article to update it
def updateSuggestedTags(esIndex,article_url, predicted_tag, ESConnector, logger):
    try:

        doc = {'doc': {'suggestedTags': [str(predicted_tag)]}}
        # This query is for elasticsearch 5.6 only
        res = ESConnector.search(index=esIndex,body={'query':{'match_all':{}},
            "_source": ["url", article_url]}, doc_type='Article')
        logger.debug(str(res))
        articleFoundID = res['hits']['hits'][0]['_id']        
        logger.debug("Article found, ID is '" + articleFoundID + "'")
        
        ESConnector.update(index=esIndex,id=int(articleFoundID), body=doc, doc_type='Article')


    except Exception as error:
        logger.critical("Error with Elasticsearch connector when trying to update an article : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector when trying to update an article  : " + str(error))
