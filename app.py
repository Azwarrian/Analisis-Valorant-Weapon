import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Valorant Weapon Analyzer", layout="wide")

# Membagi layar menjadi dua kolom: kecil untuk ikon, besar untuk teks
col1, col2 = st.columns([1, 15]) 

with col1:
    # Masukkan path gambar ikon Valorant kamu (misal logo V, ikon rank, dll)
    # Gunakan file .png dengan latar belakang transparan
    st.image("Valo.jpg", width=45)

st.title("🎯 Valorant Weapon Analyzer")
st.write("Aplikasi ini membantu kamu mencari tahu **senjata mana yang paling bagus** berdasarkan kriteria gaya bermainmu!")

# Memuat Data
@st.cache_data
def load_data():
    df = pd.read_csv("Valorant Weapon - Weapon.csv")
    # Ini WAJIB ADA untuk mengubah nama dari bahasa Inggris (CSV) ke bahasa Indonesia (Kode)
    df.columns = [
        'Weapon', 'Category', 'Kecepatan Menembak', 'Jumlah Peluru', 
        'Jarak Tembakan', 'Headshot', 'Bodyshot', 'Lowshot'
    ]
    return df

df = load_data()

# --- SIDEBAR: PENGATURAN BOBOT NILAI ---
st.sidebar.header("⚙️ Atur Kriteria Kamu")
st.sidebar.write("Geser slider untuk menentukan seberapa penting status ini bagimu (0 = Tidak Penting, 1 = Sangat Penting).")

w_fire = st.sidebar.slider("Pentingnya Kecepatan Menembak", 0.0, 1.0, 0.8)
w_mag = st.sidebar.slider("Pentingnya Jumlah Peluru", 0.0, 1.0, 0.4)
w_jar = st.sidebar.slider("Pentingnya Jarak Tembakan", 0.0, 1.0, 1.0)
w_head = st.sidebar.slider("Pentingnya Headshot", 0.0, 1.0, 1.0)
w_body = st.sidebar.slider("Pentingnya Bodyshot", 0.0, 1.0, 0.7)
w_leg = st.sidebar.slider("Pentingnya Lowshot", 0.0, 1.0, 0.3)

# --- PERHITUNGAN SKOR SENJATA ---
# Kita normalkan datanya dulu agar perhitungannya adil
cols_to_norm = ['Kecepatan Menembak', 'Jumlah Peluru', 'Jarak Tembakan', 'Headshot', 'Bodyshot', 'Lowshot']
df_norm = df.copy()

for col in cols_to_norm:
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val > min_val:
        df_norm[col] = (df[col] - min_val) / (max_val - min_val)
    else:
        df_norm[col] = 0

# Hitung nilai mentah berdasarkan settingan dari user
raw_score = (
    df_norm['Kecepatan Menembak'] * w_fire +
    df_norm['Jumlah Peluru'] * w_mag +
    df_norm['Jarak Tembakan'] * w_jar +
    df_norm['Headshot'] * w_head +
    df_norm['Bodyshot'] * w_body +
    df_norm['Lowshot'] * w_leg
)

# Konversi ke skala 0 - 100 agar mudah dibaca
if raw_score.max() > 0:
    df['Skor (0-100)'] = (raw_score / raw_score.max()) * 100
else:
    df['Skor (0-100)'] = 0

df['Skor (0-100)'] = df['Skor (0-100)'].round(2)

# Urutkan senjata dari skor yang paling bagus (tertinggi)
df_sorted = df.sort_values(by='Skor (0-100)', ascending=False).reset_index(drop=True)

# --- TAMPILAN HASIL ---
st.subheader("🏆 Peringkat Senjata Terbaik")
st.write("Semakin tinggi skornya, semakin bagus senjata tersebut berdasarkan kriteria yang kamu atur di samping.")

# Tampilkan sebagai tabel
st.dataframe(df_sorted[['Weapon', 'Category', 'Skor (0-100)', 'Jarak Tembakan', 'Headshot', 'Bodyshot']], use_container_width=True)

# Tampilkan sebagai grafik
st.subheader("📊 Top 10 Senjata Pilihanmu")
st.bar_chart(data=df_sorted.head(10), x='Weapon', y='Skor (0-100)', use_container_width=True)
