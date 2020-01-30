import unittest
import my_parser
import my_logger
import tagger_model
import language_detector
import web_scrapper

class IAeventHandlerTest(unittest.TestCase) :

    #Tests for my_parser.py :
    #Test if every arguments have been correctly parsed to the result
    def testParser(self) :
        '''result = my_parser.initParser()
        print(result.kafka_producer)
        print(result.topic)
        print(result.group_id)
        print(result.console_log_debug)
        print(result.file_log_debug)
        self.assertEqual(result.kafka_producer, )
        self.assertEqual(result.topic, )
        self.assertEqual(result.group_id, )
        self.assertEqual(result.console_log_debug, )
        self.assertEqual(result.file_log_debug, )'''
        pass

    #Tests for my_logger.py
    def testLoggerSucces(self) :

        '''ifFileDebug = False and ifConsoleLDebug = False
        logger = my_logger.initLogger(False, False)
        
        ifFileDebug = True and ifConsoleLDebug = False
        logger = my_logger.initLogger(True, False)

        ifFileDebug = False and ifConsoleLDebug = True
        logger = my_logger.initLogger(False, False)

        ifFileDebug = True and ifConsoleLDebug = True
        logger = my_logger.initLogger(True, True)'''

        pass

    
    #Tests for language_detector.py
    '''
    def testLanguageDetectionFR(self) :
        logger = my_logger.initLogger(False, False)
        language = language_detector.detect_language(logger, "Bonjour, je m'appelle Simon et j'adore faire des tests")
        self.assertEqual(language, "fr")
        pass

    def testLanguageDetectionEN(self) :
        logger = my_logger.initLogger(False, False)
        language = language_detector.detect_language(logger, "Hi my name is Simon and i love doing unnitest on Python")
        self.assertEqual(language, "en")
        pass

    def testLanguageDetectionError(self) :
        logger = my_logger.initLogger(False, False)
        with self.assertRaises(Exception): language_detector.detect_language(logger, "afazfa azdazia adncaionioanzda pozjeanzdnazndpaz azndoanzd")
        pass'''
        
    #Tests for web_scrapper.py
    '''def testWebScrapper(self) :
        logger = my_logger.initLogger(False, False)
        text = web_scrapper.news_text_recuperator(logger, "https://www.lemonde.fr/politique/article/2020/01/18/cadre-non-cadre-au-smic-a-temps-partiel-avec-enfants-ou-pas-la-reforme-des-retraites-aura-un-impact-contraste-selon-les-parcours_6026461_823448.html")
        #Test if the title has been scrapped from the article
        self.assertIn("Réforme des retraites : des conséquences très contrastées selon les parcours et les métiers",text)
        #Test if a part of the article has been scrapped
        self.assertIn("Ce sont des données attendues avec impatience.",text)
        pass'''
    
    #Tests for tagger_moddel.py
    def testTaggerModelFrArticle(self) :
        #Load model
        logger = my_logger.initLogger(False, False)
        model = tagger_model.load_model("model_fr.json", "model_fr.h5", logger)
        print(model)
        #self.assertIn("", model)

        #Prepare text
        text = web_scrapper.news_text_recuperator(logger, "https://www.lemonde.fr/politique/article/2020/01/18/cadre-non-cadre-au-smic-a-temps-partiel-avec-enfants-ou-pas-la-reforme-des-retraites-aura-un-impact-contraste-selon-les-parcours_6026461_823448.html")
        preparedText = tagger_model.prepare_text(text, "fr")
        print(preparedText)
        #self.assertIn("", preparedText)

        #Predict labels
        labels_predited = tagger_model.predict_labels(preparedText, model, "fr")
        print(labels_predited)
        #self.assertIn("", labels_predited)

        pass



if __name__ == '__main__':
    unittest.main()
        
        