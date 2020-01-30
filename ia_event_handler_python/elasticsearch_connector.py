from elasticsearch import Elasticsearch 

def createConnection(host, port, logger):
    try:
        esConnection=Elasticsearch([{'host':host ,'port':port}])
        return esConnection
    except Exception as error :
        logger.critical("Error with Elasticsearch connector : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector : " + str(error))

# WIP
def updateSuggestedTags(article_url, predicted_tag, ESConnector, logger):
    try:
        # This query is for elasticsearch 5.6 !
        res = ESConnector.search(index='Article',body={'query':{'match_all':{}},
            "_source": ["article_url", article_url]})
        logger.debug("")

    except Exception as error:
        logger.critical("Error with Elasticsearch connector : " + str(error))
        raise RuntimeError("Error with Elasticsearch connector : " + str(error))
    



