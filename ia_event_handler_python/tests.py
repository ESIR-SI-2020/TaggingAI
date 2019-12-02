import unittest
import language_detector
import Main
import my_logger
import m_parser
import web_scrapper

class IAeventHandlerTest(unittest.TestCase) :
    
    def testLogger(self) :
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        initLogger(True, True)
        sys.stdout = sys.__stdout__
        print(capturedOutput)
        
        