from preprocessing import preprocessing
import pickle
import pandas as pd

def predict(sample):
    model = pickle.load(open('knn_reg.sav', 'rb'))
    return model.predict(sample.reshape(1,-1))[0]

