import streamlit as st
import base64

st.set_page_config(page_title="My Homepage", page_icon='🏡', layout="wide")
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>',unsafe_allow_html=True)
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
.title {{
    font-family: 'TechFont', sans-serif;
    font-size: 3rem; /* Adjust the font size as needed */
    margin: 0;
    padding: 0;
    margin-bottom: 2rem;
}}
.title2 {{
    font-family: 'TechFont', sans-serif;
    font-size: 1.8rem; /* Adjust the font size as needed */
    margin: 0;
    padding: 0;
    margin-bottom: 2rem;
}}
.gradient-divider {{
    height: 3px;
    background: linear-gradient(to right, red, purple);
    border: none;
    margin-top: -20px;
    margin-bottom: 20px;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<h1 class="title">🏡 Fuel Efficiency Prediction</h1>', unsafe_allow_html=True)

st.write(' ')
col1,_,col2 = st.columns([4,0.5,5.5])

with open('images/header.png', 'rb') as f:
    image = f.read()
    col1.image(image, width=500)


col2.markdown(custom_css, unsafe_allow_html=True)
col2.markdown('<h4 class="title2">Why Fuel Efficiency Prediction Is Useful ?</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)

col2.write('Fuel efficiency prediction contributes significantly to pollution reduction by promoting the adoption of cleaner and more sustainable transportation options. By accurately forecasting fuel consumption, our project empowers individuals and businesses to make informed decisions that prioritize vehicles with lower emissions and higher fuel efficiency ratings. Moreover, our fuel efficiency prediction project facilitates the development and deployment of innovative technologies aimed at enhancing vehicle performance while minimizing environmental impact. Ultimately, our efforts in fuel efficiency prediction contribute to a cleaner, healthier planet for present and future generations.')

with col2:
    st.write(" ")
    col1, col2, col3, col4 = st.columns([3, 2.3, 2.4, 2.3])
    with col1:
        if st.button(":car: Model Finder"):
            st.switch_page("pages/2_Model_finder.py")
    with col2:
        if st.button(":bar_chart: Charts  "):
            st.switch_page("pages/3_Charts.py")
    with col3:
        if st.button("📝 Datasets  "):
            st.switch_page("pages/4_Dataset.py")
    with col4:
        if st.button("🧑‍💻 Results"):
            st.switch_page("pages/5_Results.py")
