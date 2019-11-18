import language_detector
import web_scrapper
import my_parser
import my_logger
import my_exceptions
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

# Main loop of the program
for message in kafka_consumer :
    try:
        logger.debug("kafka message received on topic ' " + results.topic + " '")
        logger.debug("  - message content : ' " + str(message) + " '.")
        url_article = message['articleUrl']
        if (url_article is not None) :
            article_text = web_scrapper.news_text_recuperator(logger, url_article)
            article_lang = language_detector.detect_language(logger, article_text)
        else :
            logger.debug("Article url not found in kafka message :" + str(message))

    except Exception as identifier:
        logger.debug("Error for kafka message : ' " + str(message) + " ', error is " + identifier)