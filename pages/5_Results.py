import streamlit as st
import pandas as pd
import os
import base64

def load_font(font_path):
    with open(font_path, "rb") as font_file:
        font_data = font_file.read()
    encoded_font = base64.b64encode(font_data).decode('utf-8')
    return encoded_font

tech_font = load_font('fonts/TECH.ttf')

custom_css = f"""
<style>
@font-face {{
    font-family: 'TechFont';
    src: url(data:font/ttf;base64,{tech_font}) format('truetype');
}}
.stTitle {{
    font-family: 'TechFont', sans-serif;
    font-size: 3rem; /* Adjust the font size as needed */
    margin: 0;
    padding: 0;
    margin-bottom: 3rem;        
}}
div.block-container {{
    padding-top: 3.5rem;
}}
.gradient-divider {{
    
    height: 4px;
    background: linear-gradient(to right, red, purple);
    border: none;
    margin-top:-20px;
    margin-bottom: 10px;
}}
</style>
"""

st.set_page_config(page_title="Model Finder",page_icon='🧑‍💻',layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<b class="stTitle">🧑‍💻Results</b><div class="gradient-divider"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([5,5])
with col1:
    st.image('images\output.png')
with col2:
    st.image('images\output2.png')   