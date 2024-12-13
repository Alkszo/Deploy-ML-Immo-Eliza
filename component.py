import streamlit as st
import pandas as pd

socecon = pd.read_csv('soceconvert.csv')
commune_names = sorted(socecon.drop_duplicates(subset='commune').commune.to_list())
zipcodes = socecon.zip_code.to_list()
commune_dict = socecon.drop_duplicates(subset='commune')[['zip_code', 'commune']].set_index('commune').to_dict()['zip_code']
zip_dict = socecon[['zip_code', 'commune']].set_index('zip_code').to_dict()['commune']
stsess = st.session_state

if 'wrong_zip_message' not in stsess:
    stsess['wrong_zip_message'] = ''


def zip_num_change():
    if stsess.zip_num not in zipcodes:
        stsess.wrong_zip_message = 'This zip code does not exist, input a valid one or select from the list'
        stsess.zip_text = None
    else:
        stsess.wrong_zip_message = ''
        stsess.zip_text = zip_dict[stsess.zip_num]

def zip_text_change():
    stsess.wrong_zip_message = ''
    if stsess.zip_text != None:
        stsess.zip_num = commune_dict[stsess.zip_text]
    else:
        stsess.zip_num = None
    

st.selectbox(label='Commune name', options=commune_names, index=89, key='zip_text', on_change=zip_text_change)
st.number_input('Zip Code:', min_value=1000, max_value=10000, value=1000, key='zip_num', on_change=zip_num_change)
st.write(stsess.wrong_zip_message)
