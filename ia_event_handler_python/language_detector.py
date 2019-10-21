import fasttext
import sys
import logging

# This function take a string and detect its language
# Return the language as acronyme
# Support only french and english for now ("fr", "en")
# Return "" if a error occured
def detect_language(article_text) :
    #reload(sys)
    #sys.setdefaultencoding('UTF8')
    lid_model = fasttext.load_model("lid.176.ftz")
    predictions = lid_model.predict(article_text)
    try:
        language = predictions[0][0].replace("__label__","").replace(" ","")
        accuracy = float(predictions[1][0])
        if accuracy < 0.5 :
            raise Exception('Accuracy too low', 'The model failed to detect precisly the article language. Accuracy : ' + str(accuracy))
        elif language != 'fr' and language != 'en' :
            raise Exception('Language unsupported', 'This article is written in an unsupported language : ' + language)
        else :
            return language
        
    except Exception as others_errors :
        logging.error("An error as occured :\n" + str(others_errors))
        return ""




