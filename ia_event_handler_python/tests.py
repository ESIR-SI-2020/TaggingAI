import unittest
import my_parser
import my_logger
import tagger_model
import language_detector
import web_scrapper
import xmlrunner
import coverage

class IAeventHandlerTest(unittest.TestCase) :

    #Tests for my_logger.py
    def testLoggerSucces(self) :

        #ifFileDebug = True and ifConsoleLDebug = True
        my_logger.initLogger(True, True)

        with open ("activity.log", "r") as myfile:
            data=myfile.readlines()

        self.assertIn('DEBUG :: Logger initialized', str(data))

        pass

    
    #Tests for language_detector.py
    def testLanguageDetectionFR(self) :
        logger = my_logger.initLogger(False, False)
        language = language_detector.detect_language(logger, "Bonjour, je m'appelle Simon et j'adore faire des tests")
        self.assertEqual(language, "fr")

    def testLanguageDetectionEN(self) :
        logger = my_logger.initLogger(False, False)
        language = language_detector.detect_language(logger, "Hi my name is Simon and i love doing unnitest on Python")
        self.assertEqual(language, "en")
        
    #Tests for web_scrapper.py
    def testWebScrapper(self) :
        logger = my_logger.initLogger(False, False)
        text = web_scrapper.news_text_recuperator(logger, "https://www.lemonde.fr/politique/article/2020/01/18/cadre-non-cadre-au-smic-a-temps-partiel-avec-enfants-ou-pas-la-reforme-des-retraites-aura-un-impact-contraste-selon-les-parcours_6026461_823448.html")
        #Test if the title has been scrapped from the article
        self.assertIn("Réforme des retraites",text)
        #Test if a part of the article has been scrapped
        self.assertIn("Ce sont des données attendues avec impatience.",text)
    
    #Tests for tagger_moddel.py
    def testTaggerModelFrArticle(self) :
        #Load model
        logger = my_logger.initLogger(False, False)
        model = tagger_model.load_model("model_en.json", "model_en.h5", logger)

        #Prepare text
        text = web_scrapper.news_text_recuperator(logger, "https://www.nytimes.com/2020/01/29/opinion/coronavirus-china-government.html")
        preparedText = tagger_model.prepare_text(text, "en")
        #print(preparedText)
        self.assertIn(0, preparedText)

        #Predict labels
        labels_predited = tagger_model.predict_labels(preparedText, model, "en")
        #print(labels_predited)
        self.assertIn("business", labels_predited)

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    with open('results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
    cov.stop()
    cov.save()
    cov.html_report()
        
        