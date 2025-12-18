import streamlit as st
import pandas as pd
import base64
from model import df, fix_unhashable, clean_coordinates, recommend_hybrid

# ----------------------------- 
# Page config & session state
# ----------------------------- 
st.set_page_config(
    page_title="Wisata Lampung Recommender",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

# ----------------------------- 
# Load & prepare data
# ----------------------------- 
df_clean = clean_coordinates(fix_unhashable(df))
PLACEHOLDER = "https://via.placeholder.com/400x250?text=No+Image"

if "Foto" not in df_clean.columns:
    df_clean["Foto"] = PLACEHOLDER
df_clean["Foto"] = df_clean["Foto"].apply(
    lambda x: x.strip() if isinstance(x, str) and x.strip() != "" else PLACEHOLDER
)

ALPHA1, ALPHA2, BETA = 0.5, 0.3, 0.2

# ----------------------------- 
# Refined CSS with Better Contrast
# ----------------------------- 
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .hero-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-bottom: 1.5rem;
        border: 4px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
        margin-bottom: 1rem;
    }
    
    .hero-description {
        font-size: 1rem;
        opacity: 0.85;
        font-weight: 300;
    }
    
    /* Filter Section */
    .filter-section {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }
    
    .filter-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .filter-subtitle {
        color: #718096;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Streamlit Select Box Styling */
    .stSelectbox > div > div {
        background-color: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        color: #2d3748;
    }
    
    .stSelectbox label {
        color: #4a5568;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Detail Page */
    .detail-header {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .detail-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    
    .detail-image-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        height: 100%;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }
    
    .info-item {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .info-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        opacity: 0.9;
    }
    
    .info-content {
        flex: 1;
    }
    
    .info-label {
        font-size: 0.85rem;
        opacity: 0.85;
        font-weight: 300;
        margin-bottom: 0.25rem;
    }
    
    .info-value {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Recommendations Section */
    .rec-section {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .rec-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .rec-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .rec-subtitle {
        color: #718096;
        font-size: 1rem;
    }
    
    /* Horizontal Scrollable Cards */
    .horizontal-scroll {
        display: flex;
        overflow-x: auto;
        gap: 1.5rem;
        padding: 1rem 0;
        scroll-behavior: smooth;
    }
    
    .horizontal-scroll::-webkit-scrollbar {
        height: 8px;
    }
    
    .horizontal-scroll::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .horizontal-scroll::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    .rec-card {
        min-width: 320px;
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .rec-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
    }
    
    .rec-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .rec-card:hover .rec-card-image {
        transform: scale(1.05);
    }
    
    .rec-card-content {
        padding: 1.5rem;
    }
    
    .rec-card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.75rem;
    }
    
    .rec-card-info {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        color: #718096;
        font-size: 0.9rem;
    }
    
    .rec-card-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Back Button */
    .back-button {
        position: fixed;
        top: 2rem;
        left: 2rem;
        z-index: 1000;
        background: white;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        font-weight: 500;
        color: #667eea;
        transition: all 0.3s ease;
    }
    
    .back-button:hover {
        transform: translateX(-5px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Modal Overlay */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .modal-content {
        background: white;
        border-radius: 20px;
        max-width: 900px;
        max-height: 90vh;
        overflow-y: auto;
        padding: 2rem;
        position: relative;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: #f7fafc;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .modal-close:hover {
        background: #e2e8f0;
        transform: rotate(90deg);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------- 
# Helper Functions
# ----------------------------- 
def load_image_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def show_hero():
    try:
        logo64 = load_image_base64("sainsdataaa.jpg")
        logo_src = f"data:image/png;base64,{logo64}" if logo64 else PLACEHOLDER
    except:
        logo_src = PLACEHOLDER
    
    st.markdown(f"""
    <div class="hero-section">
        <img src="{logo_src}" class="hero-logo" alt="Logo">
        <div class="hero-title">🌴 Jelajahi Lampung</div>
        <div class="hero-subtitle">Sistem Rekomendasi Wisata Cerdas</div>
        <div class="hero-description">Project Sains Data Kelompok 2 — Temukan destinasi impian Anda dengan teknologi AI</div>
    </div>
    """, unsafe_allow_html=True)

def go_home():
    st.session_state.page = "home"

def go_detail(place):
    st.session_state.selected_place = place
    st.session_state.page = "detail"

# ----------------------------- 
# Page: Home
# ----------------------------- 
def page_home():
    show_hero()
    
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="filter-title">🔍 Mulai Petualangan Anda</div>
    <div class="filter-subtitle">Pilih preferensi wisata dan temukan destinasi terbaik untuk Anda</div>
    """, unsafe_allow_html=True)
    
    # Filter Section
    col1, col2 = st.columns(2)
    kab_list = ["Semua Kabupaten/Kota"] + sorted(df_clean["kabupaten kota"].unique())
    selected_kab = col1.selectbox("📍 Lokasi", kab_list, key="kab_select")
    
    kat_list = ["Semua Kategori"] + sorted(df_clean["kategori"].unique())
    selected_cat = col2.selectbox("🎯 Jenis Wisata", kat_list, key="cat_select")
    
    # Filter data
    df_filtered = df_clean.copy()
    if selected_kab != "Semua Kabupaten/Kota":
        df_filtered = df_filtered[df_filtered["kabupaten kota"] == selected_kab]
    if selected_cat != "Semua Kategori":
        df_filtered = df_filtered[df_filtered["kategori"] == selected_cat]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Destination Selection
    selected_place = st.selectbox(
        "🏖️ Pilih Destinasi",
        df_filtered["Nama tempat"].tolist(),
        key="place_select"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Eksplor Destinasi & Dapatkan Rekomendasi", key="explore_btn", use_container_width=True):
        go_detail(selected_place)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- 
# Page: Detail
# ----------------------------- 
def page_detail():
    # Back Button
    if st.button("⬅ Kembali", key="back_btn"):
        go_home()
        st.rerun()
    
    place = st.session_state.selected_place
    if place is None:
        go_home()
        st.rerun()
        return
    
    # Get place details
    row = df_clean[df_clean["Nama tempat"] == place].iloc[0]
    
    st.markdown('<div class="detail-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="detail-title">{place}</div>', unsafe_allow_html=True)
    
    colA, colB = st.columns([1.3, 1.7])
    
    with colA:
        st.markdown('<div class="detail-image-container">', unsafe_allow_html=True)
        st.image(row["Foto"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with colB:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-item">
                <div class="info-icon">📂</div>
                <div class="info-content">
                    <div class="info-label">Kategori</div>
                    <div class="info-value">{row['kategori']}</div>
                </div>
            </div>
            <div class="info-item">
                <div class="info-icon">📍</div>
                <div class="info-content">
                    <div class="info-label">Lokasi</div>
                    <div class="info-value">{row['kabupaten kota']}</div>
                </div>
            </div>
            <div class="info-item">
                <div class="info-icon">🏗️</div>
                <div class="info-content">
                    <div class="info-label">Fasilitas</div>
                    <div class="info-value">{row['Fasilitas']}</div>
                </div>
            </div>
            <div class="info-item">
                <div class="info-icon">⭐</div>
                <div class="info-content">
                    <div class="info-label">Rating</div>
                    <div class="info-value">{row['rating']} / 5.0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations Section
    st.markdown("""
    <div class="rec-section">
        <div class="rec-header">
            <div class="rec-title">✨ Destinasi Serupa Untuk Anda</div>
            <div class="rec-subtitle">Berdasarkan analisis AI, berikut rekomendasi terbaik</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    rec = recommend_hybrid(
        df_clean, target=place, top_n=10, by_name=True,
        alpha1=ALPHA1, alpha2=ALPHA2, beta=BETA
    )
    
    # Create horizontal scrollable cards
    cols = st.columns(min(len(rec), 10))
    
    for idx, (i, r) in enumerate(rec.iterrows()):
        foto = r["Foto"] if isinstance(r["Foto"], str) else PLACEHOLDER
        
        with cols[idx % len(cols)]:
            if st.button("📍", key=f"rec_{idx}", use_container_width=True):
                go_detail(r['Nama tempat'])
                st.rerun()
            
            st.image(foto, use_container_width=True)
            st.markdown(f"**{r['Nama tempat']}**")
            st.caption(f"📂 {r['kategori']}")
            st.caption(f"🎯 Score: {r['score_hybrid']:.4f}")
            st.caption(f"📏 Jarak: {r['distance_km']:.2f} km")

# ----------------------------- 
# Main App
# ----------------------------- 
if st.session_state.page == "home":
    page_home()
else:
    page_detail()