import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
all_df = pd.read_csv("dashboard/all_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df['year'] = all_df['dteday'].dt.year
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Streamlit Theme
st.set_page_config(page_title="Dicoding Bikers Dashboard", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        .big-font { font-size:24px !important; }
        .highlight { background-color: #4CAF50; color: black; padding: 5px; border-radius: 5px; }
        .stApp { background-color: #000000; }
    </style>
""", unsafe_allow_html=True)

# Pilih Tahun (Slider untuk memilih tahun)
tahun = st.slider("Pilih Tahun", min_value=2011, max_value=2012, value=2011)

# Filter Data berdasarkan tahun yang dipilih
filtered_df = all_df[all_df['year'] == tahun]

# Grouping berdasarkan weekday, season, dan weathersit setelah filtering
weekday_df = filtered_df.groupby("weekday")["cnt"].mean().reset_index()
season_df = filtered_df.groupby("season")["cnt"].mean().reset_index()
weathersit_df = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()

# Judul
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚴‍♂️ Dicoding Bikers Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='big-font'>Selamat datang di Dicoding Bikers Dashboard! Mari kita eksplorasi tren penggunaan sepeda 🚲</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📆 Weekday", "⛅ Weathersit", "🌱 Season"])

# 🎨 Custom Palette
colors = sns.color_palette("coolwarm", 10)

def create_barplot(df, x_col, y_col, title, xlabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=x_col, y=y_col, data=df, palette=colors, ax=ax)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel("Jumlah Pengunjung", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    st.pyplot(fig)

with tab1:
    st.subheader("📅 Perbandingan Jumlah Peminjam untuk Setiap Hari")
    st.write("Berikut adalah perbandingan jumlah peminjam berdasarkan hari dalam seminggu:")
    
    # Group by weekday and calculate the sum of 'cnt' for the selected year
    day_df_pivot_weekday = filtered_df.groupby('weekday').agg({'cnt': 'sum'}).reset_index()

    # Display the DataFrame
    st.dataframe(day_df_pivot_weekday.style.format({"cnt": "{:.2f}"}))

    # Plot the bar chart for weekday comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(day_df_pivot_weekday['weekday'], day_df_pivot_weekday['cnt'], color='blue')
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Jumlah Peminjam')
    ax.set_title('Perbandingan Jumlah Peminjam untuk Setiap Hari')
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'])
    st.pyplot(fig)

# Pertanyaan 2 : Bagaimana perbandingan jumlah pengunjung untuk setiap weathersit?
with tab2:
    st.subheader("🌦️ Perbandingan Jumlah Peminjam Berdasarkan Cuaca")
    st.write("Bagaimana cuaca mempengaruhi jumlah peminjam sepeda?")
    
    # Map weather conditions to labels
    weather_mapping = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    filtered_df['weathersit'] = filtered_df['weathersit'].map(weather_mapping)
    
    # Group by weathersit and calculate the sum of 'cnt' for the selected year
    pivot_weathersit = filtered_df.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()

    # Display the DataFrame
    st.dataframe(pivot_weathersit.style.format({"cnt": "{:.2f}"}))

    # Plot the bar chart for weathersit comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(pivot_weathersit['weathersit'], pivot_weathersit['cnt'], color='green')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Peminjam')
    ax.set_title('Perbandingan Jumlah Peminjam Berdasarkan Kondisi Cuaca')
    st.pyplot(fig)

# Pertanyaan 3 : Bagaimana perbandingan jumlah pengunjung untuk setiap season?
with tab3:
    st.subheader("🌍 Perbandingan Jumlah Pengunjung Berdasarkan Musim")
    st.write("Berapa banyak pengunjung di setiap musim?")
    
    # Group by season and calculate the sum of 'cnt' for the selected year
    season_df = filtered_df.groupby('season')['cnt'].sum().reset_index()

    # Display the DataFrame
    st.dataframe(season_df.style.format({"cnt": "{:.2f}"}))

    # Plot the bar chart for season comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(season_df['season'], season_df['cnt'], color=['skyblue'])
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Pengunjung (cnt)')
    ax.set_title('Perbandingan Jumlah Pengunjung per Musim')
    ax.set_xticklabels(season_df['season'], rotation=45)
    st.pyplot(fig)

