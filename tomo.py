import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time


st.set_page_config(page_title="Modul Pembelajaran Tomografi", layout="wide")

st.title("🎯 Simulasi Rekonstruksi Tomografi Interaktif")


with st.expander("📖 Baca Dulu: Cara Kerja & Konsep Nyata (Klik untuk Buka)"):
    st.markdown("""
    ### Cara Kerja Sederhana:
    1. **Kita punya objek tersembunyi** (disebut *Phantom*).
    2. **Sensor membaca kepadatan** total di tiap baris (sinar horizontal) & kolom (sinar vertikal).
    3. **Kita tebak isi gambar** (dimulai dari kanvas kosong bernilai nol).
    4. **Kita koreksi tebakan** sedikit demi sedikit menggunakan algoritma ART.
    5. **Semakin banyak iterasi** → gambar akan semakin mendekati bentuk aslinya.
    
    ### Konsep Nyata di Dunia Medis/Industri:
    Metode rekonstruksi gambar seperti ini digunakan dalam:
    * **CT Scan (Medis):** Melihat organ dalam tubuh tanpa operasi.
    * **Imaging Industri:** Mendeteksi retakan di dalam beton atau pipa besi.
    
    Secara matematis, algoritma ART adalah pendekatan iteratif untuk menyelesaikan sistem persamaan linear:
    $Ax = b$
    """)
if 'n_size' not in st.session_state:
    st.session_state.n_size = 5
if 'noise_level' not in st.session_state:
    st.session_state.noise_level = 0.0
if 'lam' not in st.session_state:
    st.session_state.lam = 1.0

def generate_data():
    n = st.session_state.n_size
    noise = st.session_state.noise_level
    st.session_state.phantom = np.random.randint(1, 10, (n, n))
    st.session_state.target_rows = np.sum(st.session_state.phantom, axis=1) + np.random.normal(0, noise, n)
    st.session_state.target_cols = np.sum(st.session_state.phantom, axis=0) + np.random.normal(0, noise, n)
    st.session_state.matrix = np.zeros((n, n))
    st.session_state.history_error = []
    st.session_state.iteration = 0

if 'phantom' not in st.session_state:
    generate_data()


with st.sidebar:
    st.header("⚙️ Pengaturan Sistem")
    st.number_input("Ukuran Matriks (n)", min_value=2, max_value=20, key="n_size", on_change=generate_data)
    st.slider("Tingkat Noise Sensor", min_value=0.0, max_value=5.0, step=0.1, key="noise_level", on_change=generate_data)
    st.slider("Faktor Relaksasi (λ)", min_value=0.1, max_value=1.5, step=0.1, key="lam")
    if st.button("🔄 Buat Data Baru (Reset)", use_container_width=True):
        generate_data()

def run_art(steps):
    n = st.session_state.n_size
    lam = st.session_state.lam
    mat = st.session_state.matrix.copy()
    
    for _ in range(steps):
        for i in range(n):
            row_err = (st.session_state.target_rows[i] - np.sum(mat[i, :])) / n
            mat[i, :] += lam * row_err
        for j in range(n):
            col_err = (st.session_state.target_cols[j] - np.sum(mat[:, j])) / n
            mat[:, j] += lam * col_err
            
        mat = np.clip(mat, 0, None)
        rmse = np.sqrt(np.mean((np.sum(mat, axis=1) - st.session_state.target_rows)**2))
        st.session_state.history_error.append(rmse)
        st.session_state.iteration += 1
        
    st.session_state.matrix = mat

col1, col2, col3 = st.columns(3)
col1.metric("Iterasi Saat Ini", st.session_state.iteration)
col2.metric("Resolusi Matriks", f"{st.session_state.n_size} x {st.session_state.n_size}")

if len(st.session_state.history_error) > 0:
    last_error = st.session_state.history_error[-1]
    col3.metric("Error Sistem (RMSE)", f"{last_error:.4f}")
    
    if last_error > 5:
        st.warning("⚠️ Error masih besar → perlu lebih banyak iterasi.")
    elif last_error > 1:
        st.info("💡 Rekonstruksi mulai mendekati bentuk asli.")
    else:
        st.success("✅ Rekonstruksi sudah sangat akurat!")
else:
    col3.metric("Error Sistem (RMSE)", "Belum ada")

st.divider()

btn1, btn2, btn3, btn4 = st.columns(4)
if btn1.button("▶️ 1 Iterasi", use_container_width=True): run_art(1)
if btn2.button("⏩ 10 Iterasi", use_container_width=True): run_art(10)
if btn3.button("⏭️ 50 Iterasi", use_container_width=True): run_art(50)

if btn4.button("🎬 Animasi Auto-Play", use_container_width=True):
    for _ in range(15):
        run_art(1)
        time.sleep(0.3)
        st.rerun()

st.write("")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👁️ Perbandingan Citra", 
    "📊 Data Sensor", 
    "🔍 Error per Pixel", 
    "📈 Grafik Konvergensi", 
    "🧊 Topologi 3D", 
    "🔢 Detail Perhitungan"
])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Hasil Rekonstruksi (ART)**")
        fig_rec = px.imshow(st.session_state.matrix, text_auto=".1f", color_continuous_scale="Viridis", zmin=0, zmax=10)
        st.plotly_chart(fig_rec, use_container_width=True)
    with c2:
        st.write("**Citra Asli (Target/Phantom)**")
        fig_true = px.imshow(st.session_state.phantom, text_auto=".1f", color_continuous_scale="Viridis", zmin=0, zmax=10)
        st.plotly_chart(fig_true, use_container_width=True)

with tab2:
    st.write("Visualisasi pembacaan sensor pada sisi luar objek (Sinogram sederhana).")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("**Pembacaan Sinar Horizontal**")
        fig_bar_row = px.bar(x=range(1, st.session_state.n_size+1), y=st.session_state.target_rows, labels={'x':'Baris ke-', 'y':'Total Intensitas'})
        st.plotly_chart(fig_bar_row, use_container_width=True)
    with col_s2:
        st.write("**Pembacaan Sinar Vertikal**")
        fig_bar_col = px.bar(x=range(1, st.session_state.n_size+1), y=st.session_state.target_cols, labels={'x':'Kolom ke-', 'y':'Total Intensitas'})
        st.plotly_chart(fig_bar_col, use_container_width=True)

with tab3:
    st.write("Visualisasi ini menunjukkan letak kesalahan tebakan algoritma saat ini. Semakin mendekati nol, semakin akurat.")
    diff = st.session_state.matrix - st.session_state.phantom
    fig_diff = px.imshow(diff, text_auto=".1f", color_continuous_scale="RdBu", title="Selisih Nilai (Rekonstruksi - Asli)", color_continuous_midpoint=0)
    st.plotly_chart(fig_diff, use_container_width=True)

with tab4:
    if len(st.session_state.history_error) > 0:
        fig_err = px.line(y=st.session_state.history_error, labels={'x': 'Jumlah Iterasi', 'y': 'RMSE'})
        st.plotly_chart(fig_err, use_container_width=True)
    else:
        st.info("Jalankan iterasi untuk melihat kurva penurunan error.")

with tab5:
    st.write("Distribusi intensitas piksel dalam format elevasi 3D.")
    fig_3d = go.Figure(data=[go.Surface(z=st.session_state.matrix, colorscale="Viridis")])
    st.plotly_chart(fig_3d, use_container_width=True)

with tab6:
    st.latex(r"x^{(k+1)} = x^{(k)} + \lambda \frac{b_i - \sum x^{(k)}}{N}")
    st.write("Pilih bagian matriks untuk melihat detail perhitungannya pada kondisi saat ini:")
    
    pilihan_tipe = st.radio("Tipe Proyeksi", ["Baris", "Kolom"], horizontal=True)
    indeks_pilihan = st.selectbox("Pilih Indeks", range(1, st.session_state.n_size + 1)) - 1
    
    n = st.session_state.n_size
    lam = st.session_state.lam
    
    if pilihan_tipe == "Baris":
        target_val = st.session_state.target_rows[indeks_pilihan]
        current_val = np.sum(st.session_state.matrix[indeks_pilihan, :])
    else:
        target_val = st.session_state.target_cols[indeks_pilihan]
        current_val = np.sum(st.session_state.matrix[:, indeks_pilihan])
        
    error_val = target_val - current_val
    koreksi_val = (lam * error_val) / n
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"- Target Proyeksi ($b_i$): **{target_val:.2f}**")
        st.write(f"- Jumlah Saat Ini ($\sum x$): **{current_val:.2f}**")
        st.write(f"- Selisih: **{error_val:.2f}**")
    
    with col_b:
        st.write(f"- Jumlah Sel ($N$): **{n}**")
        st.write(f"- Faktor Relaksasi ($\lambda$): **{lam}**")
        st.info(f"Nilai penambahan untuk setiap sel: ({lam} × {error_val:.2f}) / {n} = **{koreksi_val:.2f}**")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Dibuat oleh <b>Ghazy Abiyyu Maulana</b></p>
        <p>🔗 <a href='https://github.com/Ghazy-Abiyyu-M/simulasi-tomografi' target='_blank' style='color: #4CAF50; text-decoration: none;'>Repository GitHub: Ghazy-Abiyyu-M/simulasi-tomografi</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)
