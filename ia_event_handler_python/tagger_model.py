from keras.models import model_from_json
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
import numpy
import os
import sys
import logging
import re
import langcodes
import pickle
import nltk
nltk.download('stopwords')

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
StopWordDict = {}
TokenizerDict = {}



# Function to load keras model saved into json and h5. return the fully loaded model
def load_model(model_json_name, model_h5_name, logger) :
    # Open saved model file

    # Taking account of the execution path
    executionFile = sys.argv[0]
    pathName = os.path.dirname(executionFile)
    if pathName is "" or pathName is None :
        pathName = "."

    json_file = open(pathName + "/modelTagging/" + model_json_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    # load model skeleton
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(pathName + "/modelTagging/" + model_h5_name)

    logger.debug("Model " + model_json_name + "/" + model_h5_name + " loaded")

    return loaded_model

# This function prepare the article text "one_hot encoding"
def prepare_text(article_text, article_lang) :

    # Taking account of the execution path
    executionFile = sys.argv[0]
    pathName = os.path.dirname(executionFile)
    if pathName is "" or pathName is None :
        pathName = "."

    # Lazy downloading of language stopwords
    if article_lang not in StopWordDict :
        fullLanguageName = langcodes.Language.make(language=article_lang).language_name()
        StopWordDict[article_lang] = set(stopwords.words(fullLanguageName.lower()))
    
    # Lazy loading of model Tokenizer, by language
    if article_lang not in TokenizerDict : 
        loaded_tokenizer = None
        with open(pathName + "/modelTagging/" + 'tokenizer_' + article_lang + '.pickle', 'rb') as handle:
            loaded_tokenizer = pickle.load(handle)
        TokenizerDict[article_lang] = loaded_tokenizer

    # Text processing, must be the same has the text preprocessing used for the models training
    
    article_text_prepared = REPLACE_BY_SPACE_RE.sub(' ',article_text)
    article_text_prepared = article_text_prepared.lower()
    article_text_prepared = BAD_SYMBOLS_RE.sub(' ',article_text_prepared)
    article_text_prepared = ' '.join(word for word in article_text_prepared.split() if word not in StopWordDict[article_lang]) 
    article_text_encoded = text_to_word_sequence(article_text_prepared)

    # Text tokenisation. Must have EXACTLY the same parameters than the tokenisation of the training texts
    article_text_encoded = TokenizerDict[article_lang].texts_to_sequences([article_text_encoded])

    f = open(pathName + "/modelTagging/" + 'padding_' + article_lang + '.txt', "r")
    padding = f.readline()
    f.close() 

    article_text_encoded = sequence.pad_sequences(article_text_encoded, maxlen=int(padding.replace(' ','')) ,value=0.0)

    return article_text_encoded

# This function predict the label(s) of the article using the processed text and the loaded model
def predict_labels(article_text_encoded, model, article_lang) :

    # Taking account of the execution path
    executionFile = sys.argv[0]
    pathName = os.path.dirname(executionFile)
    if pathName is "" or pathName is None :
        pathName = "."

    print(article_text_encoded.shape)
    labelRes = model.predict(article_text_encoded)
    f = open(pathName + "/modelTagging/" + 'labels_' + article_lang + '.txt', "r")
    labels = f.readline().split(",")
    f.close() 

    indexMax = numpy.argmax(labelRes)

    return labels[indexMax].replace(' ','')