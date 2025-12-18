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
# Modern CSS with Stunning Design
# ----------------------------- 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Particles Effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255,255,255,0.08) 0%, transparent 50%);
        pointer-events: none;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem 3rem 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-logo {
        width: 120px;
        height: 120px;
        margin: 0 auto 2rem auto;
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        border: 5px solid rgba(255,255,255,0.3);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        50% { transform: scale(1.05); box-shadow: 0 25px 70px rgba(0,0,0,0.4); }
    }
    
    .hero-logo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 8px 30px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    
    .hero-description {
        font-size: 1rem;
        color: rgba(255,255,255,0.85);
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Main Container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem 3rem 2rem;
    }
    
    /* Search Card - Modern & Prominent */
    .search-card {
        background: rgba(255,255,255,0.98);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 30px 90px rgba(0,0,0,0.25);
        margin-bottom: 3rem;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .search-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .search-header h2 {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .search-header p {
        color: #666;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Filter Section */
    .filter-row {
        display: grid;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Custom Selectbox */
    .stSelectbox label {
        font-weight: 600 !important;
        color: #2d3748 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 0.8rem 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
        background: white;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    /* Primary Action Button */
    .primary-action {
        margin-top: 2rem;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1.2rem 3.5rem;
        font-size: 1.15rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        width: auto;
        display: inline-block;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Back Button - Floating Style */
    .back-button-container {
        position: fixed;
        top: 2rem;
        left: 2rem;
        z-index: 1000;
    }
    
    .back-button-container button {
        background: rgba(255,255,255,0.95) !important;
        color: #667eea !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
        padding: 0.8rem 1.8rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        width: auto !important;
    }
    
    .back-button-container button:hover {
        background: white !important;
        transform: translateX(-5px) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
    }
    
    /* Detail Page */
    .detail-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 6rem 2rem 3rem 2rem;
    }
    
    .detail-hero {
        background: rgba(255,255,255,0.98);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 30px 90px rgba(0,0,0,0.25);
        margin-bottom: 3rem;
    }
    
    .detail-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .detail-image {
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        transition: all 0.5s ease;
        position: relative;
    }
    
    .detail-image::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.1) 100%);
        pointer-events: none;
    }
    
    .detail-image:hover {
        transform: scale(1.02) rotate(1deg);
        box-shadow: 0 25px 70px rgba(0,0,0,0.4);
    }
    
    .info-grid {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .info-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .info-item:hover {
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
    }
    
    .info-item:last-child {
        margin-bottom: 0;
    }
    
    .info-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        min-width: 30px;
    }
    
    .info-content {
        flex: 1;
    }
    
    .info-label {
        font-weight: 700;
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Recommendations Section */
    .rec-section {
        margin-top: 4rem;
    }
    
    .rec-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .rec-header h2 {
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .rec-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Recommendation Cards - Premium Design */
    .rec-card {
        background: rgba(255,255,255,0.98);
        border-radius: 25px;
        padding: 0;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .rec-card:hover {
        transform: translateY(-10px) scale(1.01);
        box-shadow: 0 25px 70px rgba(0,0,0,0.35);
    }
    
    .rec-card-inner {
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: 0;
        align-items: center;
    }
    
    .rec-image-wrapper {
        height: 100%;
        overflow: hidden;
        position: relative;
    }
    
    .rec-image-wrapper::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to right, transparent 0%, rgba(255,255,255,0.1) 100%);
    }
    
    .rec-content {
        padding: 2rem 2.5rem;
    }
    
    .rec-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #2d3748;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .rec-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .rec-meta-item {
        display: flex;
        align-items: center;
        color: #4a5568;
        font-size: 0.95rem;
    }
    
    .rec-meta-icon {
        margin-right: 0.5rem;
        font-size: 1.1rem;
    }
    
    .rec-meta-value {
        font-weight: 600;
        color: #2d3748;
    }
    
    .rec-button {
        display: inline-block;
    }
    
    .rec-button button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        width: auto !important;
        transition: all 0.3s ease !important;
    }
    
    .rec-button button:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Stats Badge */
    .stats-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .rec-card-inner {
            grid-template-columns: 1fr;
        }
        
        .rec-image-wrapper {
            height: 250px;
        }
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .search-card {
            padding: 2rem;
        }
        
        .detail-title {
            font-size: 2rem;
        }
        
        .back-button-container {
            position: static;
            margin-bottom: 1rem;
        }
        
        .detail-container {
            padding-top: 2rem;
        }
    }
    
    /* Hide Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
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
        <div class="hero-logo">
            <img src="{logo_src}" alt="Logo">
        </div>
        <h1 class="hero-title">🌴 Jelajahi Lampung</h1>
        <p class="hero-subtitle">Sistem Rekomendasi Wisata Cerdas</p>
        <p class="hero-description">Project Sains Data Kelompok 2 — Temukan destinasi impian Anda dengan teknologi AI</p>
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
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-header">
        <h2>🔍 Mulai Petualangan Anda</h2>
        <p>Pilih preferensi wisata dan temukan destinasi terbaik untuk Anda</p>
    </div>
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
    
    # Action Button
    st.markdown('<div class="primary-action">', unsafe_allow_html=True)
    if st.button("🚀 Eksplor Destinasi & Dapatkan Rekomendasi", key="explore_btn"):
        go_detail(selected_place)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ----------------------------- 
# Page: Detail
# ----------------------------- 
def page_detail():
    # Floating Back Button
    st.markdown('<div class="back-button-container">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="back_btn"):
        go_home()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    place = st.session_state.selected_place
    if place is None:
        go_home()
        st.rerun()
        return
    
    # Get place details
    row = df_clean[df_clean["Nama tempat"] == place].iloc[0]
    
    st.markdown('<div class="detail-container">', unsafe_allow_html=True)
    st.markdown('<div class="detail-hero">', unsafe_allow_html=True)
    
    st.markdown(f'<div class="detail-title">{place}</div>', unsafe_allow_html=True)
    
    colA, colB = st.columns([1.3, 1.7])
    
    with colA:
        st.markdown('<div class="detail-image">', unsafe_allow_html=True)
        st.image(row["Foto"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with colB:
        st.markdown(f"""
        <div class="info-grid">
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
            <h2>✨ Destinasi Serupa Untuk Anda</h2>
            <p>Berdasarkan analisis AI, berikut rekomendasi terbaik</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    rec = recommend_hybrid(
        df_clean, 
        target=place, 
        top_n=10, 
        by_name=True,
        alpha1=ALPHA1, 
        alpha2=ALPHA2, 
        beta=BETA
    )
    
    for idx, r in rec.iterrows():
        foto = r["Foto"] if isinstance(r["Foto"], str) else PLACEHOLDER
        
        st.markdown('<div class="rec-card">', unsafe_allow_html=True)
        st.markdown('<div class="rec-card-inner">', unsafe_allow_html=True)
        
        # Image Column
        st.markdown('<div class="rec-image-wrapper">', unsafe_allow_html=True)
        st.image(foto, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Content Column
        st.markdown('<div class="rec-content">', unsafe_allow_html=True)
        st.markdown(f'<div class="rec-title">{r["Nama tempat"]}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="rec-meta">
            <div class="rec-meta-item">
                <span class="rec-meta-icon">📂</span>
                <span class="rec-meta-value">{r['kategori']}</span>
            </div>
            <div class="rec-meta-item">
                <span class="rec-meta-icon">🎯</span>
                <span>Score: <span class="rec-meta-value">{r['score_hybrid']:.4f}</span></span>
            </div>
            <div class="rec-meta-item">
                <span class="rec-meta-icon">📏</span>
                <span>Jarak: <span class="rec-meta-value">{r['distance_km']:.2f} km</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="rec-button">', unsafe_allow_html=True)
        if st.button(f"Lihat Detail 👉", key=f"rec_btn_{idx}"):
            go_detail(r['Nama tempat'])
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- 
# Main App
# ----------------------------- 
if st.session_state.page == "home":
    page_home()
else:
    page_detail()