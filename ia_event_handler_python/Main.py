import language_detector
import web_scrapper
import my_parser
import my_logger
import my_exceptions
import elasticsearch_connector
import tagger_model
import kafka
import logging
from logging.handlers import RotatingFileHandler
import json

# Init parser and get all args
results = my_parser.initParser()
# Init loggers (file and console loggers)
logger = my_logger.initLogger(results.file_log_debug, results.console_log_debug)

# Generating Kafka consumer
#kafka_consumer = kafka.KafkaConsumer(
#    results.topic,
#    bootstrap_servers=[results.kafka_producer],
#    auto_offset_reset='latest',
#    enable_auto_commit=True,
#    group_id=results.group_id,
#    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#)
logger.debug("Kafka consumer initialized, with parameters ==> kafka_topic = ' " + str(results.topic) + " ', kafka_producer = ' " +
            str(results.kafka_producer) + " ' , consumer_group_id = ' " + str(results.group_id) + " '.")

# We initialize the model to None, because they are heavy and we don't know if they will be all used
modelTaggingDict = {}

# We initialize the elasticsearch connector
elasticSearchServer = results.elastic_server.split(":")
esIndex = results.elastic_index
ESConnector = elasticsearch_connector.createConnection(elasticSearchServer[0], elasticSearchServer[1], logger)
logger.debug("ESConnector initialized with " + elasticSearchServer[0] + ":" + elasticSearchServer[1])

# Main loop of the program

## For tests :
TEST = []
TEST.append({'articleUrl' : 'https://www.theguardian.com/global-development/2020/feb/07/coronavirus-chinese-rage-death-whistleblower-doctor-li-wenliang'})

# replace by 'for message in kafka_consumer :'
for message in TEST :
    try:
        logger.debug("kafka message received on topic ' " + results.topic + " '")
        logger.debug("  - message content : ' " + str(message) + " '.")
        url_article = message['articleUrl']
        if (url_article is not None) :
            
            # If the article URL exist we used it to get the article text
            article_text = web_scrapper.news_text_recuperator(logger, url_article)
            # We feed the text into our language detector function to get the correct language of thearticle
            article_lang = language_detector.detect_language(logger, article_text)
            logger.debug("Article language is " + article_lang)

            # The models are very heavy, so we lazy load them
            if article_lang not in modelTaggingDict :
                modelTaggingDict[article_lang] = tagger_model.load_model("model_" + article_lang + ".json", "model_" + article_lang + ".h5", logger)

            # We prepare the text, because we can't feed raw text to the model
            article_text_prepared = tagger_model.prepare_text(article_text, article_lang)
            
            # We used the correct model for the detected language, to get the predicted labels
            labels_predited = tagger_model.predict_labels(article_text_prepared, modelTaggingDict[article_lang], article_lang)

            logger.debug("Label(s) '" + str(labels_predited) + "' detected for the kafka message : " + str(message))

            # We try to update the suggestedTag field of the article in the elasticSearch database
            elasticsearch_connector.updateSuggestedTags(esIndex,url_article, labels_predited, ESConnector, logger)
            
        else :
            
            logger.critical("Article url not found in kafka message :" + str(message))

    except Exception as identifier:
        logger.critical("Error for kafka message : ' " + str(message) + " ', error is " + str(identifier))