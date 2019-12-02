import unittest
import Main


class IAeventHandlerTest(unittest.TestCase) :
    
    def testLogger(self) :
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        initLogger(True, True)
        sys.stdout = sys.__stdout__
        print(capturedOutput)
        
        