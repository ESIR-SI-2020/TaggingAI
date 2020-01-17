import argparse

## Initialising parameters
def initParser() :

    parser = argparse.ArgumentParser()

    parser.add_argument('-kps','--kafka_producer_server', action='store', dest='kafka_producer',
                        help="The ip/url:port of the kafka producer. Mandatory parameter.", required=True)

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
    print(results)
    return results