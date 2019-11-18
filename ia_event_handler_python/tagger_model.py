from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
import logging

# Function to load keras model saved into json and h5. return the fully loaded model
def load_model(model_json_name, model_h5_name, logger) :
    # Open saved model file
    json_file = open(model_json_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    # load model skeleton
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_h5_name)

    logger.debug("Model " + model_json_name + "/" + model_h5_name + " loaded")

    return loaded_model

