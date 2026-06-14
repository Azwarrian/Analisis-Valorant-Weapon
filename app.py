import streamlit as st
import pandas as pd
import joblib

st.title("🔫 Valorant Weapon ML Clustering")
st.write("Aplikasi ini menggunakan Machine Learning (K-Means) untuk mengelompokkan senjata Valorant berdasarkan kemiripan statistiknya.")

# 1. Load Data dan Model ML
@st.cache_data
def load_data():
    return pd.read_csv('Valorant Weapon - Weapon.csv')

@st.cache_resource
def load_models():
    # Memuat model K-Means dan Scaler dari file .pkl
    kmeans = joblib.load('kmeans_weapon_model.pkl')
    scaler = joblib.load('weapon_scaler.pkl')
    return kmeans, scaler

df = load_data()
kmeans, scaler = load_models()

# 2. Persiapkan Data untuk ML
features = df[['Fire_Rate', 'Magazine_Size', 'Damage_Head', 'Damage_Body', 'Damage_Leg']]
scaled_features = scaler.transform(features) # Gunakan scaler yang sama dari Colab

# 3. Lakukan Prediksi (Clustering)
df['ML_Cluster'] = kmeans.predict(scaled_features)

# Ubah angka cluster (0, 1, 2) menjadi nama yang lebih keren
cluster_names = {
    0: "Tipe A (Balanced/Rifle)",
    1: "Tipe B (High Damage/Sniper)",
    2: "Tipe C (High Fire Rate/SMG)"
}
df['Tipe Senjata (ML)'] = df['ML_Cluster'].map(cluster_names)

# 4. Tampilkan Hasil
st.subheader("📊 Hasil Pengelompokan Machine Learning")
st.dataframe(df[['Weapon', 'Category', 'Tipe Senjata (ML)', 'Fire_Rate', 'Damage_Head']], use_container_width=True)

# 5. Fitur Interaktif: Prediksi Senjata Kustom
st.sidebar.header("Tebak Cluster Senjata Kustom")
st.sidebar.write("Masukkan status senjata buatanmu, dan ML akan menebak ini masuk tipe apa!")

in_fire = st.sidebar.number_input("Fire Rate", min_value=0.0, value=10.0)
in_mag = st.sidebar.number_input("Magazine Size", min_value=1, value=25)
in_head = st.sidebar.number_input("Damage Head", min_value=0, value=150)
in_body = st.sidebar.number_input("Damage Body", min_value=0, value=40)
in_leg = st.sidebar.number_input("Damage Leg", min_value=0, value=30)

if st.sidebar.button("Prediksi Tipe"):
    # Buat array data baru
    new_weapon = pd.DataFrame([[in_fire, in_mag, in_head, in_body, in_leg]], 
                              columns=['Fire_Rate', 'Magazine_Size', 'Damage_Head', 'Damage_Body', 'Damage_Leg'])
    
    # Scale data baru lalu prediksi
    new_scaled = scaler.transform(new_weapon)
    prediction = kmeans.predict(new_scaled)[0]
    
    st.sidebar.success(f"Senjata buatanmu masuk kategori: **{cluster_names[prediction]}**")
