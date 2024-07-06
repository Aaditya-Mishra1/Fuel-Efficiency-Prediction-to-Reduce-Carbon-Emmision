import os
import base64
import streamlit as st
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

dataset_path = os.path.join("dataset", "Vehicle MPG - 1984 to 2023.csv")

st.set_page_config(page_title="Model Finder", page_icon=':car:', layout="wide")

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
    font-size: 3rem;
    margin: 0;
    padding: 0;
    margin-bottom: 2rem;    
}}
div.block-container {{
    padding-top: 3.5rem;
}}
.gradient-divider {{
    height: 5px;
    background: linear-gradient(to right, red, purple);
    border: none;
    margin-top: -12px;
}}
.green-number {{
    font-size: 3rem;
    color: green;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<h1 class="title">🚗 Model Finder</h1>', unsafe_allow_html=True)
df = pd.read_csv(dataset_path)

df['Fuel Efficiency (MPG)'] = df['Combined MPG (Fuel Type 1)']
co2_emission_factor = 19.6
df['Fuel Consumption (gallons/mile)'] = df['Estimated Annual Petrolum Consumption (Barrels)'] / 365
df['Carbon Emissions (g/mile)'] = (df['Fuel Consumption (gallons/mile)'] * co2_emission_factor) / df['Fuel Efficiency (MPG)']

df['Fuel MPG'] = (df['City MPG (Fuel Type 1)'] + df['Highway MPG (Fuel Type 1)']) / 2

columns_to_drop = ['Vehicle Class', 'Time to Charge EV (hours at 120v)',
                   'Time to Charge EV (hours at 240v)', 'Range (for EV)',
                   'City Range (for EV - Fuel Type 2)', 'Fuel Type 1', 'City MPG (Fuel Type 1)', 'Highway MPG (Fuel Type 1)',
                   'Hwy Range (for EV - Fuel Type 1)', 'Transmission', 'Engine Description', 'Combined MPG (Fuel Type 1)',
                   'Hwy Range (for EV - Fuel Type 2)', 'ID', 'City Range (for EV - Fuel Type 1)',
                   'City MPG (Fuel Type 2)', 'Highway MPG (Fuel Type 2)', 'Combined MPG (Fuel Type 2)',
                   'Estimated Annual Petrolum Consumption (Barrels)', 'Fuel Type 2']

df.drop(columns_to_drop, axis=1, inplace=True)
df.drop_duplicates(inplace=True)
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df.dropna(how='any', inplace=True)

max_mpg = 50
df['Fuel Efficiency (%)'] = (df['Fuel MPG'] / max_mpg) * 100

average_specific_output = 75
def round_to_nearest_ten(x):
    return int(round(x / 10) * 10)
df['Estimated Horsepower'] = df['Engine Displacement'] * average_specific_output
df['Estimated Horsepower (Rounded)'] = df['Estimated Horsepower'].apply(round_to_nearest_ten)

df.drop_duplicates(subset=['Model Year', 'Make', 'Model'], inplace=True)

col1, col2 = st.columns([3, 3])

with col1:
    year = st.slider("Select the Model Year:", 1984, 2023, (1984, 1991))
    year_start, year_end = year

    fuel_efficiency = st.slider("Select the Fuel Efficiency (%):", 0, 100, (0, 18))
    fuel_efficiency_start, fuel_efficiency_end = fuel_efficiency

    cylinders = st.slider("Select the number of Cylinders:", 4, 10, (4, 5))
    cylinders_start, cylinders_end = cylinders

    horsepower = st.slider("Select the horsepower:", 0, 1000, (0, 162))
    horsepower_start, horsepower_end = horsepower

    filtered_df = df[
        (df['Engine Cylinders'] >= cylinders_start) & (df['Engine Cylinders'] <= cylinders_end) &
        (df['Estimated Horsepower (Rounded)'] >= horsepower_start) & (df['Estimated Horsepower (Rounded)'] <= horsepower_end) &
        (df['Model Year'] >= year_start) & (df['Model Year'] <= year_end) &
        (df['Fuel Efficiency (%)'] >= fuel_efficiency_start) & (df['Fuel Efficiency (%)'] <= fuel_efficiency_end)
    ]

    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df['Serial'] = filtered_df.index + 1
    

    st.markdown(f'<h3>Number of Available Car Models: <span class="green-number">{len(filtered_df)}</span></h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h3>Available Car Models</h3>', unsafe_allow_html=True)    
    
    selected_columns = filtered_df[['Model Year', 'Make', 'Model']]
    st.dataframe(selected_columns, height=400, use_container_width=True)

with col2:
    filtered_df['Year_Make_Model_Drive'] = filtered_df['Model Year'].astype(str) + ' ' + filtered_df['Make'] + ' ' + filtered_df['Model'] + ' ' + filtered_df['Drive']
    selected_make_model = st.selectbox("Select Year Make and Model of the car:", filtered_df['Year_Make_Model_Drive'].tolist())
    selected_rows = filtered_df[filtered_df['Year_Make_Model_Drive'] == selected_make_model]
    st.write(' ')

    if not selected_rows.empty:
        selected_row = selected_rows.iloc[0]
        fuel_efficiency_value = selected_row['Fuel Efficiency (%)']

        efficiency_color = f"hsl({(fuel_efficiency_value / 100) * 120}, 100%, 50%)"

        st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <h1 style='color: {efficiency_color}; font-size: 380px; font-weight: bold; margin-top: -90px; line-height: 1;'>{int(fuel_efficiency_value)}</h1>
                <h2 style='color: {efficiency_color}; font-size: 70px; font-weight: bold; margin-top: -28px;'>% Efficiency</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style='border:2px solid #ccc; padding: 10px; border-radius: 10px; margin-top: 20px;'>
                <h3>Car Model Details</h3>
                <p><strong>Model Year:</strong> {selected_row['Model Year']}</p>
                <p><strong>Make:</strong> {selected_row['Make']}</p>
                <p><strong>Model:</strong> {selected_row['Model']}</p>
                <p><strong>Drive:</strong> {selected_row['Drive']}</p>
                <p><strong>Engine Displacement:</strong> {selected_row['Engine Displacement']}</p>
                <p><strong>Engine Cylinders:</strong> {selected_row['Engine Cylinders']}</p>
                <p><strong>Estimated Horsepower:</strong> {selected_row['Estimated Horsepower (Rounded)']}</p>
                <p><strong>Fuel Efficiency (MPG):</strong> {selected_row['Fuel MPG']}</p>
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("""
    <style>
    .stSelectbox div[role='listbox'] {{
        height: 3.5rem;
        font-size: 1.2rem;
    }}
    .stTitle {{
        height: 3.5rem;
        font-size: 2rem;
    }}
    </style>
    """, unsafe_allow_html=True)
