from preprocessor import Preprocessor
from KNNModel import KNNModel
import pandas as pd

processor = Preprocessor(pd.read_csv('data/cleaned-data.csv'), pd.read_csv('data/soceconvert.csv'))
model = KNNModel(processor.get_train_test())

model.evaluate_model()