import pandas as pd
import statistics
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import resreg
import seaborn as sns

class Preprocessor:
    """
    The class encompasing various functions and operations preparing the dataset to be fed into the model
    """

    def __init__(self, dataframe, socecon):
        """
        Initializing data preprocessor, class takes the main self.dataframe and socioeconomic data acquired from open sources
        """
        self.dataframe = dataframe
        self.socecon = socecon

    
    def add_socecon(self):
        """
        Method adding socioeconomic data to main dataframe
        """
        self.dataframe = pd.merge(self.dataframe, self.socecon.drop(columns=['refnis', 'province', 'commune']), on='zip_code', how='left')

    def drop_outliers(self):
        """
        This method eliminates price and living area outliers from dataframe with cut-off point at 3 stdev over mean
        """
        price_bound = round(statistics.mean(self.dataframe.price) + statistics.stdev(self.dataframe.price) * 3)
        self.dataframe = self.dataframe.loc[self.dataframe['price'] < price_bound]        

        area_bound = round(statistics.mean(self.dataframe.living_area) + statistics.stdev(self.dataframe.living_area) * 3)
        self.dataframe = self.dataframe.loc[self.dataframe['living_area'] < area_bound]

        self.dataframe.reset_index(inplace=True)
        self.dataframe.drop(columns=['index'], inplace=True)  

    def remove_unneaded(self):
        """
        Method to remove columns that are irrelevant for further modelling, it also removes rows containing 'other property' type, which appears unfrequently and constitutes noise in the data.
        """
        self.dataframe.drop(columns=['zip_code', 'commune', 'facade_number', 'furnished', 'open_fire', 'sub_property_group_encoded'], inplace=True)
        self.dataframe = self.dataframe[self.dataframe.subtype_of_property != 'other property']

    def encode_variables(self):
        """
        Method to numerically encode remaining categorical values 
        """
        #this mapping breakes down different types of properties into 4 categories: 1 = budget, 2 = residential, 3 = whole building, 4 = exclusive
        type_of_property_mapping = {'service flat': 1, 'flat studio': 1, 'chalet': 1, 'kot': 1, 'house': 2, 'apartment': 2, 'ground floor': 2, 'town house': 2, 'bungalow': 2, 
                        'duplex': 3, 'apartment block': 3, 'triplex': 3, 'farmhouse': 3, 'country cottage': 3, 'mixed use building': 3, 'manor house': 4, 'exceptional property': 4, 'villa': 4, 'penthouse': 4, 'mansion': 4, 'loft': 4}

        self.dataframe['subtype_of_property'] = self.dataframe['subtype_of_property'].map(type_of_property_mapping)

        #mapping of provinces
        province_mapping = {
        'Bruxelles': 11,
        'West-Vlaanderen': 10,
        'Vlaams Brabant': 9,    
        'Brabant Wallon': 8,
        'Antwerpen': 7,    
        'Oost-Vlaanderen': 6,
        'Limburg': 5,
        'Luxembourg': 4,
        'Namur': 3,
        'Liège': 2,
        'Hainaut': 1
        }
        self.dataframe['province'] = self.dataframe['province'].map(province_mapping)

        #mapping of building condition
        building_condition_mapping = {
        'good': 3,
        'no info': 2,
        'to renovate': 1,
        'to restore': 0
        }
        self.dataframe['building_condition'] = self.dataframe['building_condition'].map(building_condition_mapping)

        #mapping kitchen
        kitchen_mapping = {
            'equipped': 2,
            'installed': 1,
            'not installed': 0
        }
        self.dataframe['equipped_kitchen'] = self.dataframe['equipped_kitchen'].map(kitchen_mapping)

    def dataset_cleaning(self):
        """
        A comprehensive method that performs all the steps necessary to get clean and encoded dataframe
        """
        self.add_socecon()
        self.drop_outliers()
        self.remove_unneaded()
        self.encode_variables()

    def get_Xy(self) -> tuple:
        """
        Method returning features and target from cleaned dataset
        """
        self.dataset_cleaning()
        y = self.dataframe['price']
        X = self.dataframe.drop(['price'], axis=1)

        return X, y
    
    def get_train_test(self) -> tuple:
        """
        This method performs splits the data into training and testing set to be fed to model, it also resamples dataset to account for unequal datapoints distribution
        """
        X, y = self.get_Xy()
        scaler = MinMaxScaler(feature_range=(0,1))
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=11, test_size=0.2)
        relevance = resreg.sigmoid_relevance(y_train, cl=np.percentile(y_train, 15), ch=np.percentile(y_train, 75))
        X_train, y_train = resreg.smoter(X_train, y_train, relevance, relevance_threshold=0.4, over='balance', random_state=11)
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.fit_transform(X_test)

        return X_train, X_test, y_train, y_test



test_processor = Preprocessor(pd.read_csv('data/cleaned-data.csv'), pd.read_csv('data/soceconvert.csv'))


