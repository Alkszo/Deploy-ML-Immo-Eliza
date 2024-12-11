import pandas as pd
from sklearn.preprocessing import MinMaxScaler

socecon = pd.read_csv('model/data/soceconvert.csv')
scale_matrix = pd.read_csv('model/scaling_matrix.csv')

def preprocessing(input):
    processed = pd.merge(input, socecon.drop(columns=['refnis', 'commune']), on='zip_code', how='left')
    processed.drop(columns=['zip_code'], inplace=True)

    type_of_property_mapping = {'service flat': 1, 'flat studio': 1, 'chalet': 1, 'kot': 1, 'house': 2, 'apartment': 2, 'ground floor': 2, 'town house': 2, 'bungalow': 2, 
                        'duplex': 3, 'apartment block': 3, 'triplex': 3, 'farmhouse': 3, 'country cottage': 3, 'mixed use building': 3, 'manor house': 4, 'exceptional property': 4, 'villa': 4, 'penthouse': 4, 'mansion': 4, 'loft': 4}

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
    
    building_condition_mapping = {
        'good': 3,
        'no info': 2,
        'to renovate': 1,
        'to restore': 0
        }
    
    kitchen_mapping = {
            'equipped': 2,
            'installed': 1,
            'not installed': 0
        }

    processed['subtype_of_property'] = processed['subtype_of_property'].map(type_of_property_mapping)
    processed['province'] = processed['province'].map(province_mapping)
    processed['building_condition'] = processed['building_condition'].map(building_condition_mapping)
    processed['equipped_kitchen'] = processed['equipped_kitchen'].map(kitchen_mapping)

    to_scale = pd.concat([scale_matrix, processed])
    scaler = MinMaxScaler(feature_range=(0,1))
    to_scale = scaler.fit_transform(to_scale)
    

    return to_scale[-1]
