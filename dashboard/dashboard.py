import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import seaborn as sns
import streamlit as st

#create weekday tabel 
def create_weekday_tabel(df):
    weekday_per_tahun=df[df['year'] == tahun]
    weekday_tabel = weekday_per_tahun.groupby(by=['weekday']).agg({"cnt": "mean"})
    return weekday_tabel

#create season tabel 
def create_season_tabel(df):
    season_per_tahun=df[df['dteday'].dt.year == tahun]
    season_tabel = season_per_tahun.groupby(by="season").agg({"cnt": "mean"})
    return season_tabel

#create weathersit tabel 
def create_weathersit_tabel(df):
    weathersit_per_tahun=df[df['year'] == tahun]
    weathersit_tabel = weathersit_per_tahun.groupby(by=['weathersit']).agg({
        "cnt": "mean"
    })
    return weathersit_tabel

def create_hum_tabel(df):
    hum_per_tahun=df[df['year'] == tahun]
    hum_tabel = df[['hum','cnt']]
    return hum_tabel

# Memasukkan data 
all_df = pd.read_csv("dashboard\all_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df['year'] = all_df['dteday'].dt.year
all_df.sort_values(by="dteday", inplace=True)
all_df['year'] = all_df['dteday'].dt.year
all_df.reset_index(inplace=True)

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df['year'] = all_df['dteday'].dt.year
all_df.reset_index(inplace=True)

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

#Membuat dataset 
tahun = st.selectbox(label = 'Choose The Year', options = (2011,2012), key='year_selectbox')
weekday_df=create_weekday_tabel(all_df)
season_df=create_season_tabel(all_df)
weathersit_df=create_weathersit_tabel(all_df)
hum_df=create_hum_tabel(all_df)

#Membuat bagian pertama dashboard
st.title("Dicoding Bikers Dashboard")
st.header("Let's Bike!!")
st.text('Hello Bikers! Welcome to Dicoding Bikers Dashboard! Lets explore about the truth of our service.')
tahun = st.selectbox(
    label = 'Choose The Year',
    options = (2011,2012)
    )
st.write('Your Choose: ', tahun)
tab1, tab2, tab3= st.tabs(["Weekday","Weathersit","Season"])

#membuat bagian tab
with tab1 : 
    fig, ax = plt.subplots(nrows=1, figsize=(30, 6))

    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    sns.barplot(x='weekday', y='cnt', data=weekday_df.sort_values(by='cnt', ascending=False))
    ax.set_ylabel("Jumlah Pengunjung")
    ax.set_xlabel("Hari")
    ax.set_title("Jumlah pengunjung setiap harinya", loc="center", fontsize=18)
    ax.tick_params(axis ='y', labelsize=15)

    st.pyplot(fig)

with tab2 : 
    fig, ax = plt.subplots(nrows=1, figsize=(30, 6))

    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    sns.barplot(x='weathersit', y='cnt', data=weathersit_df.sort_values(by='cnt', ascending=False))
    ax.set_ylabel("Jumlah Pengunjung")
    ax.set_xlabel("Cuaca")
    ax.set_title("Jumlah pengunjung setiap cuaca", loc="center", fontsize=18)
    ax.tick_params(axis ='y', labelsize=15)

    st.pyplot(fig)

with tab3: 
    fig, ax = plt.subplots(nrows=1, figsize=(30, 6))

    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    sns.barplot(x='season', y='cnt', data=season_df.sort_values(by='cnt', ascending=False))
    ax.set_ylabel("Jumlah Pengunjung")
    ax.set_xlabel("Season")
    ax.set_title("Jumlah pengunjung setiap seasonnya", loc="center", fontsize=18)
    ax.tick_params(axis ='y', labelsize=15)

    st.pyplot(fig)
