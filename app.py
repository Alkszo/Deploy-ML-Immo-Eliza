import streamlit as st
import pandas as pd
from preprocessing import preprocessing
from predict import predict
socecon = pd.read_csv('soceconvert.csv')
commune_names = sorted(socecon.drop_duplicates(subset='commune').commune.to_list())
zipcodes = socecon.zip_code.to_list()
commune_dict = socecon.drop_duplicates(subset='commune')[['zip_code', 'commune']].set_index('commune').to_dict()['zip_code']
zip_dict = socecon[['zip_code', 'commune']].set_index('zip_code').to_dict()['commune']

st.set_page_config(
    page_title="Real Estate Price Predictions",
    page_icon="🏘️",
    layout="centered",
)

st.header('Input property characteristics')

stsess = st.session_state

#initialize necessary session states
if 'wrong_zip_message' not in stsess:
    stsess['wrong_zip_message'] = ''

if 'df_results' not in stsess:
    stsess['df_results'] = pd.DataFrame(columns = ['predicted price', 'property type', 'locality', 'zipcode', 'living area', 'bedroom nr', 'terrace m2', 'garden m2', 'land plot m2', 'building condition', 'kitchen state', 'swimming pool'])

#utility functions for synchronizing inputs between different types of widgets
def zip_num_change() -> None:
    if stsess.zip_num not in zipcodes:
        stsess.wrong_zip_message = 'This zip code does not exist, input a valid one or select from the list'
        stsess.zip_text = None
    else:
        stsess.wrong_zip_message = ''
        stsess.zip_text = zip_dict[stsess.zip_num]

def zip_text_change() -> None:
    stsess.wrong_zip_message = ''
    if stsess.zip_text != None:
        stsess.zip_num = commune_dict[stsess.zip_text]
    else:
        stsess.zip_num = None

def update_plot_slide() -> None:
    stsess.plot_surface_slide = stsess.plot_surface_num

def update_plot_num() -> None:
    stsess.plot_surface_num = stsess.plot_surface_slide

def update_living_slide() -> None:
    stsess.living_area_slide = stsess.living_area_num

def update_living_num() -> None:
    stsess.living_area_num = stsess.living_area_slide

def update_garden_slide() -> None:
    stsess.garden_slide = stsess.garden_num

def update_garden_num() -> None:
    stsess.garden_num = stsess.garden_slide

def reset_outside() -> None:
    stsess.garden_num = 0
    stsess.garden_slide = 0
    stsess.plot_surface_num = 0
    stsess.plot_surface_slide = 0

#main site content, inputs of real estate properties
type_of_property = st.radio('House or Apartment:', ['House', 'Apartment'], on_change=reset_outside)
if type_of_property == 'House':
    subtype_of_property = st.selectbox('Type of property:', ['house', 'chalet', 'town house', 'bungalow', 'duplex', 'apartment block', 'triplex', 'farmhouse', 'country cottage', 'mixed use building', 'manor house', 'exceptional property', 'villa', 'mansion'])
else:
    subtype_of_property = st.selectbox('Type of property:', ['apartment', 'service flat', 'flat studio','kot', 'ground floor', 'exceptional property', 'penthouse', 'loft' ])
st.divider()
st.selectbox(label='Commune name', options=commune_names, index=89, key='zip_text', on_change=zip_text_change)
st.selectbox(label='Zip Code:', options=zipcodes, key='zip_num', on_change=zip_num_change)
st.write(stsess.wrong_zip_message)
st.divider()
living_area_num = st.number_input('Living Area:', min_value=10, max_value=400, value=100, key='living_area_num', on_change=update_living_slide)
living_area_slide = st.slider('Living Area:', min_value=10, max_value=400, value=100, key='living_area_slide', label_visibility='hidden', on_change=update_living_num)
st.divider()
bedroom_nr = st.slider('Number of Bedrooms:', min_value=0, max_value=10, value=2)
terrace = st.slider('Terrace surface:', min_value=0, max_value=100, value=10)
st.divider()
if type_of_property == 'House':
    garden_num = st.number_input('Garden space:', min_value=0, max_value=500, value=0, key='garden_num', on_change=update_garden_slide)
    garden_slide = st.slider('Garden space:', min_value=0, max_value=500, value=0, key='garden_slide', label_visibility='hidden', on_change=update_garden_num)
else:
    garden_num = st.number_input('Garden space:', min_value=0, max_value=500, value=0, key='garden_num', on_change=update_garden_slide, disabled=True)
    garden_slide = st.slider('Garden space:', min_value=0, max_value=500, value=0, key='garden_slide', label_visibility='hidden', on_change=update_garden_num, disabled=True)
st.divider()
if type_of_property == 'House':
    plot_surface_num = st.number_input('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_num', on_change=update_plot_slide)
    plot_surface_slide = st.slider('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_slide', label_visibility='hidden', on_change=update_plot_num)
else:
    plot_surface_num = st.number_input('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_num', on_change=update_plot_slide, disabled=True)
    plot_surface_slide = st.slider('Land plot surface:', min_value=0, max_value=1000, value=0, key='plot_surface_slide', label_visibility='hidden', on_change=update_plot_num, disabled=True)
st.divider()
col1, buff, col2 = st.columns([2,1,2])
with col1: 
    building_condition = st.select_slider('Building condition:', ['good', 'no info', 'to renovate'])
with col2:
    equipped_kitchen = st.select_slider('Kitchen:', ['equipped', 'installed', 'not installed'])
swimming_pool = st.radio('Property has swimming pool:', ['No', 'Yes'])

#price predict button calling the model and adding results to queries history dataframe
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
        d = {'type_of_property': [type_of_property], 'zip_code': [stsess.zip_num], 'living_area': [stsess.living_area_num], 'bedroom_nr': [bedroom_nr], 'terrace': [terrace], 'garden': [stsess.garden_num], 'plot_surface': [stsess.plot_surface_num],
             'subtype_of_property': [subtype_of_property], 'building_condition': [building_condition], 'equipped_kitchen': [equipped_kitchen], 'swimming_pool': [swimming_pool]}
        df_input = pd.DataFrame(data=d)             
        input_transformed = preprocessing(df_input)
        prediction = '{:,.0f}'.format(round(predict(input_transformed)))
        st.success(f"The predicted price of this property is {prediction} €")

        stsess.df_results = pd.concat([stsess.df_results, pd.DataFrame({'predicted price': [prediction], 'property type': [subtype_of_property], 'locality': [stsess.zip_text], 'zipcode': [stsess.zip_num], 
        'living area': [stsess.living_area_num], 'bedroom nr': [bedroom_nr], 'terrace m2': [terrace], 'garden m2': [stsess.garden_num], 'land plot m2': [stsess.plot_surface_num], 
        'building condition': [building_condition], 'kitchen state': [equipped_kitchen], 'swimming pool': [swimming_pool]})], ignore_index=True)
        
    except:
        st.success(f"Invalid input, check zip code and try again")
        
#function do download query resolts
@st.cache_data
def convert_df(df) -> None:
    return df.to_csv(index=False).encode("utf-8")

#display query history and download buttn
if len(stsess.df_results) > 0:
    csv_file = convert_df(stsess.df_results)
    st.write('Previous queries')
    st.dataframe(stsess.df_results)
    st.download_button(label='download results as csv', data=csv_file, mime="text/csv", file_name='price predictions.csv')