import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import seaborn as sb 
import streamlit as st
import tensorflow as tf 
from tensorflow import keras 
from keras import layers 
import plotly.graph_objs as go
import plotly.express as px
import warnings 
warnings.filterwarnings('ignore')
import tensorflow as tf
from keras.src.callbacks.early_stopping import EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

st.set_page_config(page_title="Log Files",page_icon='🗃️',layout="wide")
st.title("🗃️ DevLog - Check Terminal")
st.markdown('<style>div.block-container{padding-top:1.5rem;}</style>',unsafe_allow_html=True)
dataset_path = os.path.join("dataset", "Vehicle MPG - 1984 to 2023.csv")
df = pd.read_csv(dataset_path)

df['Fuel Efficiency (MPG)'] = df['Combined MPG (Fuel Type 1)']
co2_emission_factor = 19.6
df['Fuel Consumption (gallons/mile)'] = df['Estimated Annual Petrolum Consumption (Barrels)'] / 365
df['Carbon Emissions (g/mile)'] = (df['Fuel Consumption (gallons/mile)'] * co2_emission_factor) / df['Fuel Efficiency (MPG)']


columns_to_drop = ['Vehicle Class', 'Time to Charge EV (hours at 120v)', 
                   'Time to Charge EV (hours at 240v)', 'Range (for EV)', 
                    'City Range (for EV - Fuel Type 2)','Fuel Type 1','Drive','City MPG (Fuel Type 1)','Highway MPG (Fuel Type 1)',
                   'Hwy Range (for EV - Fuel Type 1)', 'Transmission','Engine Description','Combined MPG (Fuel Type 1)',
                   'Hwy Range (for EV - Fuel Type 2)','ID', 'City Range (for EV - Fuel Type 1)',
                   'City MPG (Fuel Type 2)','Highway MPG (Fuel Type 2)','Combined MPG (Fuel Type 2)',
                   'Estimated Annual Petrolum Consumption (Barrels)','Fuel Type 2']

df.drop(columns_to_drop, axis=1, inplace=True)
df.drop_duplicates(inplace=True)
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df.dropna(how='any', inplace=True)

import category_encoders as ce
categorical_columns = df.select_dtypes(include=['object']).columns
target_encoder = ce.TargetEncoder(cols=categorical_columns)
data_encoded = target_encoder.fit_transform(df[categorical_columns], df['Fuel Efficiency (MPG)'])
df[categorical_columns] = data_encoded

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[df_scaled.columns[:-1]] = scaler.fit_transform(df_scaled[df_scaled.columns[:-1]])

from sklearn.model_selection import train_test_split
features = df.drop(['Fuel Efficiency (MPG)'], axis=1)
target = df['Fuel Efficiency (MPG)']
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def train_regression_model(X_train, y_train, X_test, y_test, epochs=100, l2_penalty=0.01):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2_penalty)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2_penalty)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mape'])

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, 
                        validation_data=(X_test, y_test), callbacks=[early_stopping], verbose=1)

    return model, history

best_model, history = train_regression_model(X_train, y_train, X_test, y_test, epochs=100, l2_penalty=0.01)
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100 
print("Mean Squared Error (MSE):", mse)
print("Mean Absolute Percentage Error (MAPE):", mape)

losses = pd.DataFrame(history.history)
history_df = pd.DataFrame(history.history) 

epochs_to_display = 60
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=list(range(epochs_to_display)), 
    y=history.history['loss'][:epochs_to_display], 
    mode='lines', 
    name='Training Loss'
))
fig1.add_trace(go.Scatter(
    x=list(range(epochs_to_display)), 
    y=history.history['val_loss'][:epochs_to_display], 
    mode='lines', 
    name='Validation Loss',
    line=dict(color='red')
))
fig1.update_layout(title='Training and Validation Loss', xaxis_title='Epochs', yaxis_title='Loss')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=list(range(epochs_to_display)), 
    y=history.history['mape'][:epochs_to_display], 
    mode='lines', 
    name='Training MAPE'
))
fig2.add_trace(go.Scatter(
    x=list(range(epochs_to_display)), 
    y=history.history['val_mape'][:epochs_to_display], 
    mode='lines', 
    name='Validation MAPE',
    line=dict(color='red')
))
fig2.update_layout(title='Training and Validation MAPE', xaxis_title='Epochs', yaxis_title='MAPE')


col1,col2=st.columns([5,5])
with col1:
    st.plotly_chart(fig1,use_container_width=True)

with col2:
    st.plotly_chart(fig2,use_container_width=True)