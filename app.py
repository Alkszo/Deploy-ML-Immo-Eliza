import streamlit as st
import pandas as pd
from preprocessing import preprocessing
from predict import predict

st.header('Input property characteristics')

type_of_property = st.radio('House or Apartment:', ['House', 'Apartment'])
zip_code = st.number_input('Zip Code:', min_value=1000, max_value=10000, value=1000)
living_area = st.slider('Living Area:', min_value=10, max_value=450, value=100)
bedroom_nr = st.slider('Number of Bedrooms:', min_value=0, max_value=10, value=2)
terrace = st.slider('Terrace space:', min_value=0, max_value=100, value=10)
garden = st.slider('Garden space:', min_value=0, max_value=1000, value=0)
plot_surface = st.slider('Land plot surface:', min_value=0, max_value=1000, value=0)
subtype_of_property = st.selectbox('Type of property:', ['house', 'apartment', 'service flat', 'flat studio', 'chalet', 'kot', 'ground floor', 'town house', 'bungalow', 'duplex', 'apartment block', 'triplex', 'farmhouse', 'country cottage', 'mixed use building', 'manor house', 'exceptional property', 'villa', 'penthouse', 'mansion', 'loft'])
building_condition = st.select_slider('Building condition:', ['no info', 'good', 'to renovate', 'to restore'])
equipped_kitchen = st.select_slider('Kitchen:', ['equipped', 'installed', 'not installed'])
swimming_pool = st.radio('Property has swimming pool:', ['No', 'Yes'])

if st.button('Predict Price'):
    try:
        if type_of_property == 'House':
            type_of_property = 1
        else:
            type_of_property = 0

        if swimming_pool == 'Yes':
            swimming_pool = 1
        else:
            swimming_pool = 0
        d = {'type_of_property': [type_of_property], 'zip_code': [zip_code], 'living_area': [living_area], 'bedroom_nr': [bedroom_nr], 'terrace': [terrace], 'garden': [garden], 'plot_surface': [plot_surface],
             'subtype_of_property': [subtype_of_property], 'building_condition': [building_condition], 'equipped_kitchen': [equipped_kitchen], 'swimming_pool': [swimming_pool]}
        df_input = pd.DataFrame(data=d)
        input_transformed = preprocessing(df_input)
        prediction = '{:,.0f}'.format(round(predict(input_transformed)))
        st.success(f"The predicted price of this property is {prediction} €")
        
    except:
        st.success(f"You can't afford any property. Should have eaten less avocado toasts!")