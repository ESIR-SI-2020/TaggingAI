import language_detector
import web_scrapper
import my_parser
import my_logger
import my_exceptions
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
kafka_consumer = kafka.KafkaConsumer(
    results.topic,
    bootstrap_servers=[results.kafka_producer],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=results.group_id,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
logger.debug("Kafka consumer initialized, with parameters ==> kafka_topic = ' " + results.topic + " ', kafka_producer = ' " +
            results.kafka_producer + " ' , consumer_group_id = ' " + results.group_id + " '.")

# We initialize the model to None, because they are heavy and we don't know if they will be all used
modelTaggingEn = None
modelTaggingFr = None
labels_predited = None

# Main loop of the program
for message in kafka_consumer :
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

            # The models are heavy, so we load them the first time a specific language model is needed
            if (article_lang is "en" and modelTaggingEn is None) :
                modelTaggingEn = tagger_model.load_model("","",logger)
            if (article_lang is "fr" and modelTaggingFr is None) :
                modelTaggingFr = tagger_model.load_model("","",logger)

            # We prepare the text, because we can't feed raw text to the model
            article_text_prepared = tagger_model.prepare_text(article_text)
            
            # We used the correct model for the detected language, to get the predicted labels
            if (article_lang is "en") :
                labels_predited = tagger_model.predict_labels(article_text_prepared, modelTaggingEn)
            elif (article_lang is "fr") :
                labels_predited = tagger_model.predict_labels(article_text_prepared, modelTaggingFr)

            logger.debug("Label(s) '" + str(labels_predited) + "' detected for the kafka message : " + str(message))
            
        else :
            logger.critical("Article url not found in kafka message :" + str(message))

    except Exception as identifier:
        logger.critical("Error for kafka message : ' " + str(message) + " ', error is " + identifier)