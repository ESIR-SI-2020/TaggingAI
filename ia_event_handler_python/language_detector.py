import fasttext
import sys
import logging

# This function takes a string and detect its language
# Return the language as an acronyme
# Supports french and english for now ("fr", "en")

def detect_language(logger, article_text) :
    SUPPORTED_LANGUAGES = ['fr','eng']
    #reload(sys)
    #sys.setdefaultencoding('UTF8')
    lid_model = fasttext.load_model("lid.176.ftz")
    predictions = lid_model.predict(article_text)
    try:
        language = predictions[0][0].replace("__label__","").replace(" ","")
        accuracy = float(predictions[1][0])
        if accuracy < 0.5 :
            raise Exception('Accuracy too low', 'The model failed to detect precisly the article language. Accuracy: ' + str(accuracy))
        elif language not in SUPPORTED_LANGUAGES :
            raise Exception('Language unsupported', 'This article is written in an unsupported language: ' + language)
        else :
            return language
        
    except Exception as other_errors :
        logger.error("'detect_language' ==> An error occured: \n" + str(other_errors))
        raise other_errors
