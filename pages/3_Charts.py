import streamlit as st              #python -m pip install -U streamlit
import pandas as pd                 #python -m pip install -U pandas
import matplotlib.pyplot as plt     #python -m pip install -U matplotlib
import seaborn as sb                #python -m pip install -U seaborn   
import plotly.tools
import plotly.express as px
import os
import base64           

import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")

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
    margin-bottom: 2rem;        
}}
div.block-container {{
    padding-top: 3.5rem;
}}
</style>
"""


st.set_page_config(page_title="Charts", page_icon=':bar_chart:', layout="wide")

st.markdown(custom_css, unsafe_allow_html=True)


st.markdown('<h1 class="stTitle">📊 Charts</h1>', unsafe_allow_html=True)

dataset_path = os.path.join("dataset", "Vehicle MPG - 1984 to 2023.csv")
df = pd.read_csv(dataset_path)
df['Fuel Efficiency (MPG)'] = df['Combined MPG (Fuel Type 1)']
co2_emission_factor = 19.6
df['Fuel Consumption (gallons/mile)'] = df['Estimated Annual Petrolum Consumption (Barrels)'] / 365  
df['Carbon Emissions (g/mile)'] = (df['Fuel Consumption (gallons/mile)'] * co2_emission_factor) / df['Fuel Efficiency (MPG)']

col1, col2 = st.columns([5, 5])
divider_style = """
<style>
.gradient-divider {
    
    height: 4px;
    background: linear-gradient(to right, red, purple);
    border: none;
    margin-top:-12px;
}
</style>
"""
with col1:
    company_carbon = df.groupby('Make')['Carbon Emissions (g/mile)'].mean()
    company_carbon_sorted = company_carbon.sort_values(ascending=True)
    top_10 = company_carbon_sorted.head(10)
    st.markdown(divider_style, unsafe_allow_html=True)
    st.markdown(f'<h4>Top 10 Car Manufacturers with Lowest Carbon Emission</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)
    
    
    color_scale = [(0, "green"), (1, "yellow")]
    
    fig = px.bar(top_10, 
                 x=top_10.values, 
                 y=top_10.index, 
                 orientation='h', 
                 template='seaborn',
                 color=top_10.values, 
                 color_continuous_scale=color_scale)
    
    fig.update_layout(xaxis=dict(title="Mean Carbon Emission (g/mile)", title_font=dict(color="white")),
                      coloraxis_showscale=True,
                      yaxis=dict(title="Car Manufacturer", title_font=dict(color="white")), 
                      yaxis_autorange="reversed")
    
    st.plotly_chart(fig, use_container_width=True, height=400)

    
with col2:
    company_emissions = df.groupby('Make')['Carbon Emissions (g/mile)'].sum()
    sorted_companies = company_emissions.sort_values(ascending=False)
    top_10_companies = sorted_companies.head(10)
    top_10_companies = top_10_companies.sort_values(ascending=True)
    st.markdown(divider_style, unsafe_allow_html=True)
    st.markdown(f'<h4>Top 10 Car Manufacturers with Highest Total Carbon Emission</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)
    

    color_scale = [(0, "orange"), (1, "red")]

    fig = px.bar(top_10_companies, 
             x=top_10_companies.values, 
             y=top_10_companies.index, 
             orientation='h',
             template='seaborn', 
             color=top_10_companies.values, 
             color_continuous_scale=color_scale)

    fig.update_layout(xaxis=dict(title="Total Carbon Emission (g/mile)", title_font=dict(color="white")),
                  yaxis=dict(title="Car Manufacturer", title_font=dict(color="white")), 
                  yaxis_categoryorder='total ascending')

    st.plotly_chart(fig, use_container_width=True, height=400)

df_2023 = df[df['Model Year'] == 2023]
total_emission_by_company = df_2023.groupby('Make')['Carbon Emissions (g/mile)'].sum()
sorted_companies = total_emission_by_company.sort_values()

st.markdown(divider_style, unsafe_allow_html=True)
st.markdown(f'<h4>Total Carbon Emission by Car Company in 2023</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)

color_scale = [(0, "green"), (0.25, "yellow"), (0.5, "orange"), (1, "red")]

fig = px.bar(sorted_companies, 
             x=sorted_companies.values, 
             y=sorted_companies.index, 
             orientation='h',
             labels={'x': 'Total Carbon Emission (g/mile)', 'y': 'Car Company'}, 
             width=1000, 
             height=900,
             color=sorted_companies.values,
             color_continuous_scale=color_scale,
             color_continuous_midpoint=sorted_companies.values.mean()
            )

fig.update_layout(xaxis_title='Total Carbon Emission (g/mile)', 
                  yaxis_title='Car Company', 
                  yaxis=dict(categoryorder='total ascending'),
                  plot_bgcolor='rgba(0,0,0,0)', 
                  showlegend=False)

st.plotly_chart(fig, use_container_width=True)


mean_emission_by_year = df.groupby('Model Year')['Carbon Emissions (g/mile)'].mean()

st.markdown(divider_style, unsafe_allow_html=True)
st.markdown(f'<h4>Trend of Carbon Emissions Over the Years</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)

fig_line = px.line(mean_emission_by_year, x=mean_emission_by_year.index, y=mean_emission_by_year.values,
                   template='seaborn', markers=True)
fig_line.update_traces(line=dict(color='red'))
fig_line.update_layout(xaxis=dict(title="Model Year", title_font=dict(color="white")),
                       yaxis=dict(title="Mean Carbon Emission (g/mile)", title_font=dict(color="white")),
                       xaxis_showgrid=True, yaxis_showgrid=True)
st.plotly_chart(fig_line, use_container_width=True)

top_companies = df.groupby('Make')['Carbon Emissions (g/mile)'].sum().nlargest(10).index.tolist()
years = []
max_emissions = []

for company in top_companies:
    max_emission_year = df[df['Make'] == company].groupby('Model Year')['Carbon Emissions (g/mile)'].sum().idxmax()
    max_emission = df[(df['Make'] == company) & (df['Model Year'] == max_emission_year)]['Carbon Emissions (g/mile)'].iloc[0]
    years.append(max_emission_year)
    max_emissions.append(max_emission)

st.markdown(divider_style, unsafe_allow_html=True)
st.markdown(f'<h4>Max Carbon Emission by Top Car Manufacturers in a Year</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)

df_max_emissions = pd.DataFrame({'Car Manufacturer': top_companies, 'Max Carbon Emission': max_emissions})


color_scale = [(0, "orange"), (1, "red")]

fig = px.bar(df_max_emissions, 
             x='Car Manufacturer', 
             y='Max Carbon Emission', 
             template='seaborn',
             color='Max Carbon Emission', 
             color_continuous_scale=color_scale)

fig.update_layout(xaxis=dict(title="Car Manufacturer", title_font=dict(color="white")),
                  yaxis=dict(title="Max Carbon Emission", title_font=dict(color="white")),
                  xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

df_1984 = df[df['Model Year'] == 1984]
total_emission_1984 = df_1984.groupby('Make')['Carbon Emissions (g/mile)'].sum()
total_emission_2023 = df_2023.groupby('Make')['Carbon Emissions (g/mile)'].sum()
comparison_df = pd.concat([total_emission_1984, total_emission_2023], axis=1)
comparison_df.columns = ['Total Emission 1984', 'Total Emission 2023']
comparison_df = comparison_df.fillna(0)
st.markdown(divider_style, unsafe_allow_html=True)
st.markdown(f'<h4>Total Carbon Emissions by Car Company: 1984 vs 2023</h4><p class="gradient-divider"></p>', unsafe_allow_html=True)
fig = px.line(comparison_df, x=comparison_df.index, y=['Total Emission 1984', 'Total Emission 2023'],
              template='seaborn', markers=True, color_discrete_sequence=['red', 'skyblue'], height=600, width=1200)
fig.update_layout(xaxis=dict(title="Car Company", title_font=dict(color="white")),
                  yaxis=dict(title="Total Carbon Emission (g/mile)", title_font=dict(color="white")),
                  xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                  font=dict(color="white"), legend=dict(font=dict(color="white")))
st.plotly_chart(fig)
