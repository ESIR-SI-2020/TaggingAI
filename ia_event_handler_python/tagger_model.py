from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
import sys
import logging

# Function to load keras model saved into json and h5. return the fully loaded model
def load_model(model_json_name, model_h5_name, logger) :
    # Open saved model file
    executionFile = sys.argv[0]
    pathName = os.path.dirname(executionFile)
    json_file = open(pathName + "/modelTagging/" + model_json_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    # load model skeleton
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(pathName + "/modelTagging/" + model_h5_name)

    logger.debug("Model " + model_json_name + "/" + model_h5_name + " loaded")

    return loaded_model

# TODO
# This function prepare the article text "one_hot encoding"
def prepare_text(article_text) :
    pass # TODO
    return []

# TODO
# This function predict the label(s) of the article using the processed text and the loaded model
def predict_labels(article_text_encoded, model) :
    pass # TODO
    return []