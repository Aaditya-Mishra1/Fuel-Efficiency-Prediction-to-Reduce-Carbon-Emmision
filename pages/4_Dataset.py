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
    margin-bottom: -2rem;        
}}
div.block-container {{
    padding-top: 3.5rem;
}}
</style>
"""

st.set_page_config(page_title="Dataset Viewer", page_icon='📝', layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<h1 class="stTitle">📝 DataSet</h1>', unsafe_allow_html=True)
dataset_path = os.path.join("dataset", "Vehicle MPG - 1984 to 2023.csv")
df = pd.read_csv(dataset_path)
total_rows = len(df)

divider_style = """
<style>
.gradient-divider {
    
    height: 4px;
    background: linear-gradient(to right, red, purple);
    border: none;
    margin-top:-20px;
    margin-bottom: 10px;
}
</style>
"""

st.markdown(divider_style, unsafe_allow_html=True)
st.markdown(f'<h2>Total Dataset Available:<b style="color:green; font-size: 5rem;"> {total_rows}</b></h2><div class="gradient-divider"></div>', unsafe_allow_html=True)
st.dataframe(df)


