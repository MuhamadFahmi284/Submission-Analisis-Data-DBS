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

# Pilih Tahun
tahun = st.slider("Pilih Tahun", min_value=2011, max_value=2012, value=2011)

# Filter Data
weekday_df = all_df[all_df['year'] == tahun].groupby("weekday")["cnt"].sum().reset_index()
season_df = all_df[all_df['year'] == tahun].groupby("season")["cnt"].sum().reset_index()
weathersit_df = all_df[all_df['year'] == tahun].groupby("weathersit")["cnt"].sum().reset_index()

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
    st.subheader("📅 Jumlah Pengunjung per Hari")
    st.write("Berikut adalah rata-rata jumlah pengunjung per hari dalam setahun:")
    st.dataframe(weekday_df.style.format({"cnt": "{:.2f}"}))
    create_barplot(weekday_df, "weekday", "cnt", "Jumlah Pengunjung Berdasarkan Hari", "Hari")

with tab2:
    st.subheader("🌦️ Pengaruh Cuaca terhadap Jumlah Pengunjung")
    st.write("Bagaimana cuaca mempengaruhi jumlah pengunjung sepeda?")
    st.dataframe(weathersit_df.style.format({"cnt": "{:.2f}"}))
    create_barplot(weathersit_df, "weathersit", "cnt", "Jumlah Pengunjung Berdasarkan Cuaca", "Cuaca")

with tab3:
    st.subheader("🌍 Jumlah Pengunjung Berdasarkan Musim")
    st.write("Berapa banyak pengunjung di setiap musim?")
    st.dataframe(season_df.style.format({"cnt": "{:.2f}"}))
    create_barplot(season_df, "season", "cnt", "Jumlah Pengunjung Berdasarkan Musim", "Musim")
