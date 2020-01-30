import fasttext
import sys
import os
import logging

# This function takes a string and detect its language
# Return the language as an acronyme
# Supports french and english for now ("fr", "en")
SUPPORTED_LANGUAGES = ['fr','en']

def detect_language(logger, article_text) :
    
    # Taking account of the execution path
    executionFile = sys.argv[0]
    pathName = os.path.dirname(executionFile)
    if pathName is "" or pathName is None :
        pathName = "."
        
    lid_model = fasttext.load_model(pathName + "/lid.176.ftz")
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
