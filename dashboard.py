import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from babel.numbers import format_currency

# Konfigurasi Tampilan Streamlit
st.set_page_config(page_title="📊 Dashboard Analisis Penjualan", layout="wide")

# Sidebar Profil
st.sidebar.image("https://www.w3schools.com/w3images/avatar2.png", width=150)
st.sidebar.title("Profil Mahasiswa")
st.sidebar.write("Nama  : Bayu Prasetyo")
st.sidebar.write("NIM   : 10122308 ")
st.sidebar.write("Kelas : IF 5")

# Sidebar Navigasi
menu = st.sidebar.radio("Menu", ["Beranda", "SOAL NO 1", "SOAL NO 2"])


# Memuat data dari URL
product_url = "https://raw.githubusercontent.com/Byy21/Tubes-UAS-PDSD/main/products_dataset.csv"
customer_url = "https://raw.githubusercontent.com/Byy21/Tubes-UAS-PDSD/main/customers_dataset.csv"
seller_url = "https://raw.githubusercontent.com/Byy21/Tubes-UAS-PDSD/main/sellers_dataset.csv"

try:
    df = pd.read_csv(product_url)
    customer_df = pd.read_csv(customer_url)
    seller_df = pd.read_csv(seller_url)
    
    if menu == "Beranda":
        st.title("📊 Dashboard Analisis Penjualan")
        st.write("Selamat datang di aplikasi analisis data produk dan pelanggan.")
        st.image("https://raw.githubusercontent.com/Byy21/Tubes-UAS-PDSD/main/db_analisis.png", use_column_width=True)
    elif menu == "SOAL NO 1":
        st.title("SOAL NO 1")
        st.subheader("Soal 1")
        st.write("Menampilkan data dari dataset produk dengan product_name_lenght lebih besar dari 63.0")
        
        # Menampilkan data produk
        st.subheader("Data Produk")
        st.write(df.head())
        
        # Soal 1: Menampilkan produk dengan product_name_lenght > 63.0
        panjang_nama_produk = df[df['product_name_lenght'] > 63.0]
        st.subheader("Produk dengan Nama Lebih Panjang dari 63 Karakter")
        st.write(panjang_nama_produk)
        
        # Visualisasi hubungan panjang nama produk vs panjang deskripsi
        st.subheader("Visualisasi Panjang Nama Produk vs Panjang Deskripsi")
        fig, ax = plt.subplots()
        ax.scatter(panjang_nama_produk.product_description_lenght, panjang_nama_produk.product_name_lenght, alpha=0.5)
        ax.set_xlabel("Panjang Deskripsi Produk")
        ax.set_ylabel("Panjang Nama Produk")
        ax.set_title("Hubungan Panjang Nama dan Deskripsi Produk")
        st.pyplot(fig)
        
        # Filter kategori moveis_decoracao
        moveis_decoracao = df[df['product_category_name'] == 'moveis_decoracao']
        jumlah = moveis_decoracao[moveis_decoracao['product_name_lenght'] > 63.0]
        st.subheader("Produk dalam Kategori 'moveis_decoracao' dengan Nama Lebih Panjang dari 63 Karakter")
        st.write(jumlah)
        
        # Visualisasi panjang deskripsi vs panjang nama produk
        st.subheader("Grafik Panjang Deskripsi vs Panjang Nama Produk")
        fig, ax = plt.subplots()
        ax.plot(jumlah.product_description_lenght, jumlah.product_name_lenght)
        ax.set_xlabel("Panjang Deskripsi Produk")
        ax.set_ylabel("Panjang Nama Produk")
        ax.set_title("Hubungan Panjang Deskripsi dan Nama Produk")
        st.pyplot(fig)
    
    elif menu == "SOAL NO 2":
        st.title("SOAL NO 2")
        st.subheader("Soal 2")
        st.write("Menampilkan kota dengan jumlah pelanggan terbanyak dan kota dengan jumlah pelanggan paling sedikit, serta nilainya.")
        
        # Menampilkan data pelanggan
        st.subheader("Data Pelanggan")
        st.write(customer_df.head())
        
        # Mengecek Missing Values
        st.subheader("Cek Missing Values pada Data Pelanggan")
        st.write(customer_df.isna().sum())
        
        # Mengecek Duplikasi Data
        st.subheader("Cek Duplikasi Data pada Data Pelanggan")
        st.write(customer_df.duplicated().sum())
        
        # Mengecek Tipe Data
        st.subheader("Tipe Data pada Data Pelanggan")
        st.write(customer_df.dtypes)
        
        # Analisis pelanggan per kota
        customer_city = customer_df['customer_city'].value_counts()
        seller_city = seller_df['seller_city'].value_counts()
        
        kota_terbanyak = customer_city.idxmax()
        jumlah_terbanyak = customer_city.max()
        kota_terkecil = customer_city.idxmin()
        jumlah_terkecil = customer_city.min()
        
        st.subheader("Jawaban Soal 2: Kota dengan Pelanggan Terbanyak dan Paling Sedikit")
        st.write(f"Kota dengan pelanggan terbanyak: {kota_terbanyak} ({jumlah_terbanyak} pelanggan)")
        st.write(f"Kota dengan pelanggan paling sedikit: {kota_terkecil} ({jumlah_terkecil} pelanggan)")
        
        # Grafik pelanggan dan seller terbanyak
        st.subheader("Grafik 5 Kota dengan Customer dan Seller Terbanyak")
        warna = ['green', 'lightgreen', 'lightgreen', 'lightgreen', 'yellow']
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        
        axes[0].bar(customer_city.head(5).index, customer_city.head(5).values, color=warna)
        axes[0].set_xticklabels(customer_city.head(5).index, rotation=90)
        axes[0].set_title('5 Kota Customer Terbanyak')
        
        axes[1].bar(seller_city.head(5).index, seller_city.head(5).values, color=warna)
        axes[1].set_xticklabels(seller_city.head(5).index, rotation=90)
        axes[1].set_title('5 Kota Seller Terbanyak')
        
        plt.tight_layout()
        st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")