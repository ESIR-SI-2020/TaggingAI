import language_detector
import web_scrapper
import argparse
import kafka
import logging
from logging.handlers import RotatingFileHandler
import json

# Clean parsing options with temp examples
## Initialising parameters
parser = argparse.ArgumentParser()

parser.add_argument('-kps','--kafka_producer_server', action='store', dest='kafka_producer',
                    help="The ip/url:port of the kafka producer. Mandatory parameter.")

parser.add_argument('-tn','--topic_name',default='ARTICLE_ADDED',action='store',dest='topic',
                    help="Let you specify the Kafka topic name. Events in your topic should respect the default topic structure. default topic is 'ARTICLE_ADDED'")

parser.add_argument('-gi','--group_id',default=0,type=int,action='store',dest='group_id',
                    help="Let you specify the Kafka groupid. default group id is 0")

parser.add_argument("-v", "--verbose", help="increase output verbosity by switching console log level to debug.", dest='console_log_debug',
                    action="store_true")

parser.add_argument("-vf", "--verbose_file", help="increase output verbosity by switching file log level to debug.", dest='file_log_debug',
                    action="store_true")

parser.add_argument('--version', action='version', version='%(prog)s 0.0')

results = parser.parse_args()

# Setting the logging
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
logger.setLevel(logging.DEBUG)

## file logger handler
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
if results.file_log_debug :
    file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
## console logger handler
stream_handler = logging.StreamHandler()
if results.console_log_debug :
    stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

## send warning in log for log level
if results.console_log_debug :
    logger.warning('CONSOLE LOG DEBUG MODE ACTIVATED')

if results.file_log_debug :
    logger.warning('FILE LOG DEBUG MODE ACTIVATED')

logger.debug('Logger initialized')

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

        article_text = web_scrapper.news_text_recuperator(logger, url_article)
        article_lang = language_detector.detect_language(logger, article_text)

    except Exception as identifier:
        pass
    



    






