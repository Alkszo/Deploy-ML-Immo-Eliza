import streamlit as st
import pandas as pd
from preprocessing import preprocessing
from predict import predict

st.header('Input property characteristics')

stsess = st.session_state

def update_plot_slide():
    stsess.plot_surface_slide = stsess.plot_surface_num

def update_plot_num():
    stsess.plot_surface_num = stsess.plot_surface_slide

def update_living_slide():
    stsess.living_area_slide = stsess.living_area_num

def update_living_num():
    stsess.living_area_num = stsess.living_area_slide

def update_garden_slide():
    stsess.garden_slide = stsess.garden_num

def update_garden_num():
    stsess.garden_num = stsess.garden_slide

type_of_property = st.radio('House or Apartment:', ['House', 'Apartment'])
zip_code = st.number_input('Zip Code:', min_value=1000, max_value=10000, value=1000)
living_area_num = st.number_input('Living Area:', min_value=10, max_value=400, value=100, key='living_area_num', on_change=update_living_slide)
living_area_slide = st.slider('Living Area:', min_value=10, max_value=400, value=100, key='living_area_slide', label_visibility='hidden', on_change=update_living_num)
bedroom_nr = st.slider('Number of Bedrooms:', min_value=0, max_value=10, value=2)
terrace = st.slider('Terrace surface:', min_value=0, max_value=100, value=10)
garden_num = st.number_input('Garden space:', min_value=0, max_value=500, value=0, key='garden_num', on_change=update_garden_slide)
garden_slide = st.slider('Garden space:', min_value=0, max_value=500, value=0, key='garden_slide', label_visibility='hidden', on_change=update_garden_num)
plot_surface_num = st.number_input('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_num', on_change=update_plot_slide)
plot_surface_slide = st.slider('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_slide', label_visibility='hidden', on_change=update_plot_num)
if type_of_property == 'House':
    subtype_of_property = st.selectbox('Type of property:', ['house', 'chalet', 'town house', 'bungalow', 'duplex', 'apartment block', 'triplex', 'farmhouse', 'country cottage', 'mixed use building', 'manor house', 'exceptional property', 'villa', 'mansion'])
else:
    subtype_of_property = st.selectbox('Type of property:', ['apartment', 'service flat', 'flat studio','kot', 'ground floor', 'exceptional property', 'penthouse', 'loft' ])
col1, buff, col2 = st.columns([2,1,2])
with col1: 
    building_condition = st.select_slider('Building condition:', ['no info', 'good', 'to renovate'])
with col2:
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
        d = {'type_of_property': [type_of_property], 'zip_code': [zip_code], 'living_area': [stsess.living_area_num], 'bedroom_nr': [bedroom_nr], 'terrace': [terrace], 'garden': [stsess.garden_num], 'plot_surface': [stsess.plot_surface_num],
             'subtype_of_property': [subtype_of_property], 'building_condition': [building_condition], 'equipped_kitchen': [equipped_kitchen], 'swimming_pool': [swimming_pool]}
        df_input = pd.DataFrame(data=d)
        #st.dataframe(df_input)
        input_transformed = preprocessing(df_input)
        prediction = '{:,.0f}'.format(round(predict(input_transformed)))
        st.success(f"The predicted price of this property is {prediction} €")
        
    except:
        st.success(f"You can't afford any property. Should have eaten less avocado toasts!")