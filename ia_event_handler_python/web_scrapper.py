import requests
from bs4 import BeautifulSoup
import logging

# Function to extract title and text of an article from an URL
# Return a string
# Return "" if a error occured
def news_text_recuperator(logger, url) :
    try:
        raw_soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        logger.debug("news_text_recuperator : data recovered from " + str(url))
        news_title = raw_soup.find('title').get_text()
        news_content_tab = raw_soup.find_all('p')
        news_content = ""
        for paragraphe in news_content_tab : 
            news_content = news_content + " " + paragraphe.get_text()
        news_content = news_content.replace(u'\xa0', u' ').replace(u'\n', ' ').replace(u'\\', '')
        return news_title + " " + news_content

    except requests.exceptions.ContentDecodingError as request_decoding_error:
        logger.error("'news_text_recuperator' ==> Request module content decoding error :\n" + str(request_decoding_error))
        raise request_decoding_error

    except Exception as others_errors :
        logger.error("'news_text_recuperator' ==> An error as occured :\n" + str(others_errors))
        raise others_errors