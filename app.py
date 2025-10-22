import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import time
from tsp_solver import (
    generate_cities, 
    precompute_distances,
    solve_nn_all_starts,
    solve_insertion_all_starts,
    solve_ci_all_starts,
    three_opt,
    calculate_tour_distance
)

# Konfigurasi halaman
st.set_page_config(
    page_title="TSP Optimizer",
    page_icon="🗺️",
    layout="wide"
)

# CSS Custom
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'cities_data' not in st.session_state:
    st.session_state.cities_data = None
if 'results_history' not in st.session_state:
    st.session_state.results_history = []
if 'dist_matrix' not in st.session_state:
    st.session_state.dist_matrix = None

# Header
st.markdown('<div class="main-header">🗺️ TSP Heuristic Optimizer</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar untuk Input
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # Pilihan input data
    input_method = st.radio(
        "Pilih Metode Input:",
        ["Generate Random", "Upload CSV"],
        help="Pilih cara memasukkan data kota"
    )
    
    if input_method == "Generate Random":
        st.subheader("Generate Data Random")
        num_cities = st.slider("Jumlah Kota:", 5, 50, 15)
        max_x = st.number_input("Max X Koordinat:", 100, 2000, 1000)
        max_y = st.number_input("Max Y Koordinat:", 100, 2000, 1000)
        
        if st.button("🎲 Generate Cities", use_container_width=True):
            with st.spinner("Generating cities..."):
                st.session_state.cities_data = generate_cities(num_cities, max_x, max_y)
                cities_list = list(st.session_state.cities_data.keys())
                st.session_state.dist_matrix = precompute_distances(cities_list, st.session_state.cities_data)
                st.success(f"✅ {num_cities} kota berhasil di-generate!")
    
    else:
        st.subheader("Upload File CSV")
        
        # Download template CSV
        template_df = pd.DataFrame({
            'city_id': [1, 2, 3, 4, 5],
            'x': [100, 300, 500, 700, 900],
            'y': [200, 400, 100, 500, 300]
        })
        
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template CSV",
            data=csv_template,
            file_name="template_cities.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.info("Format CSV: city_id, x, y")
        
        uploaded_file = st.file_uploader(
            "Upload file CSV:",
            type=['csv'],
            help="File harus memiliki kolom: city_id, x, y"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validasi kolom
                required_cols = ['city_id', 'x', 'y']
                if not all(col in df.columns for col in required_cols):
                    st.error(f"❌ File harus memiliki kolom: {', '.join(required_cols)}")
                else:
                    # Konversi ke format yang dibutuhkan
                    cities_data = {}
                    for _, row in df.iterrows():
                        cities_data[int(row['city_id'])] = {
                            'X': float(row['x']),
                            'Y': float(row['y'])
                        }
                    
                    st.session_state.cities_data = cities_data
                    cities_list = list(cities_data.keys())
                    st.session_state.dist_matrix = precompute_distances(cities_list, cities_data)
                    st.success(f"✅ {len(cities_data)} kota berhasil di-upload!")
            
            except Exception as e:
                st.error(f"❌ Error membaca file: {str(e)}")
    
    st.markdown("---")
    
    # Pilihan Metode Heuristik
    st.subheader("🔧 Pilih Metode Heuristik")
    
    methods = {
        'Nearest Neighbor': st.checkbox("Nearest Neighbor (NN)", value=True),
        'Nearest Insertion': st.checkbox("Nearest Insertion (NI)", value=True),
        'Farthest Insertion': st.checkbox("Farthest Insertion (FI)", value=True),
        'Cheapest Insertion': st.checkbox("Cheapest Insertion (CI)", value=True),
        'Arbitrary Insertion': st.checkbox("Arbitrary Insertion (AI)", value=False)
    }
    
    if methods['Arbitrary Insertion']:
        ai_runs = st.number_input("AI Runs per Start:", 1, 20, 5)
    else:
        ai_runs = 5
    
    st.markdown("---")
    
    # Opsi 3-Opt
    st.subheader("🎯 Optimasi Lanjutan")
    use_3opt = st.checkbox("Gunakan 3-Opt Optimization", value=True)
    
    st.markdown("---")
    
    # Tombol Run
    run_button = st.button("▶️ Run Optimization", use_container_width=True, type="primary")

# Main Content Area
if st.session_state.cities_data is None:
    st.info("👈 Silakan generate atau upload data kota terlebih dahulu dari sidebar")
else:
    # Display current cities
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 Visualisasi Kota")
        
        # Plot cities
        cities_df = pd.DataFrame([
            {'id': k, 'x': v['X'], 'y': v['Y']} 
            for k, v in st.session_state.cities_data.items()
        ])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=cities_df['x'],
            y=cities_df['y'],
            mode='markers+text',
            marker=dict(size=12, color='red'),
            text=cities_df['id'],
            textposition='top center',
            name='Cities'
        ))
        
        fig.update_layout(
            title="Posisi Kota",
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            hovermode='closest',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Informasi Data")
        st.metric("Jumlah Kota", len(st.session_state.cities_data))
        
        # Tampilkan data kota
        with st.expander("Lihat Data Kota"):
            st.dataframe(cities_df, use_container_width=True)

# Run Optimization
if run_button and st.session_state.cities_data is not None:
    selected_methods = [k for k, v in methods.items() if v]
    
    if not selected_methods:
        st.error("❌ Pilih minimal satu metode heuristik!")
    else:
        st.markdown("---")
        st.subheader("🔄 Proses Optimasi")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        cities_list = list(st.session_state.cities_data.keys())
        dist_matrix = st.session_state.dist_matrix
        
        results = []
        total_methods = len(selected_methods)
        
        for idx, method in enumerate(selected_methods):
            status_text.text(f"⏳ Running {method}...")
            start_time = time.time()
            
            # Run construction heuristic
            if method == 'Nearest Neighbor':
                tour, distance = solve_nn_all_starts(cities_list, dist_matrix)
            elif method == 'Nearest Insertion':
                tour, distance = solve_insertion_all_starts(cities_list, dist_matrix, 'nearest')
            elif method == 'Farthest Insertion':
                tour, distance = solve_insertion_all_starts(cities_list, dist_matrix, 'farthest')
            elif method == 'Cheapest Insertion':
                tour, distance = solve_ci_all_starts(cities_list, dist_matrix)
            elif method == 'Arbitrary Insertion':
                tour, distance = solve_insertion_all_starts(cities_list, dist_matrix, 'arbitrary', num_runs=ai_runs)
            
            construction_time = time.time() - start_time
            initial_distance = distance
            
            # Run 3-Opt if enabled
            if use_3opt:
                status_text.text(f"⏳ Running 3-Opt on {method}...")
                start_opt = time.time()
                tour, distance = three_opt(tour, dist_matrix)
                opt_time = time.time() - start_opt
            else:
                opt_time = 0
            
            improvement = ((initial_distance - distance) / initial_distance * 100) if use_3opt else 0
            
            results.append({
                'Method': method,
                'Initial Distance': round(initial_distance, 2),
                'Final Distance': round(distance, 2),
                'Improvement (%)': round(improvement, 2),
                'Construction Time (s)': round(construction_time, 3),
                '3-Opt Time (s)': round(opt_time, 3),
                'Total Time (s)': round(construction_time + opt_time, 3),
                'Tour': tour
            })
            
            progress_bar.progress((idx + 1) / total_methods)
        
        status_text.text("✅ Optimasi selesai!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # Save to history
        st.session_state.results_history.append({
            'timestamp': pd.Timestamp.now(),
            'num_cities': len(cities_list),
            'use_3opt': use_3opt,
            'results': results
        })
        
        # Display results
        st.markdown("---")
        st.subheader("📈 Hasil Optimasi")
        
        # Results table
        results_df = pd.DataFrame([
            {k: v for k, v in r.items() if k != 'Tour'}
            for r in results
        ])
        results_df = results_df.sort_values('Final Distance')
        
        st.dataframe(
            results_df.style.highlight_min(subset=['Final Distance'], color='lightgreen'),
            use_container_width=True
        )
        
        # Best result visualization
        st.markdown("---")
        st.subheader("🏆 Visualisasi Rute Terbaik")
        
        best_result = min(results, key=lambda x: x['Final Distance'])
        best_tour = best_result['Tour']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Metode Terbaik", best_result['Method'])
        col2.metric("Jarak Total", f"{best_result['Final Distance']:.2f}")
        col3.metric("Total Waktu", f"{best_result['Total Time (s)']:.3f}s")
        
        # Plot best tour
        tour_coords = [st.session_state.cities_data[city_id] for city_id in best_tour]
        tour_coords.append(tour_coords[0])  # Close the loop
        
        fig = go.Figure()
        
        # Plot route lines
        fig.add_trace(go.Scatter(
            x=[c['X'] for c in tour_coords],
            y=[c['Y'] for c in tour_coords],
            mode='lines',
            line=dict(color='blue', width=2),
            name='Route'
        ))
        
        # Plot cities
        fig.add_trace(go.Scatter(
            x=[c['X'] for c in tour_coords[:-1]],
            y=[c['Y'] for c in tour_coords[:-1]],
            mode='markers+text',
            marker=dict(size=12, color='red'),
            text=best_tour,
            textposition='top center',
            name='Cities'
        ))
        
        # Highlight start city
        start_city = st.session_state.cities_data[best_tour[0]]
        fig.add_trace(go.Scatter(
            x=[start_city['X']],
            y=[start_city['Y']],
            mode='markers',
            marker=dict(size=20, color='green', symbol='star'),
            name='Start/End'
        ))
        
        fig.update_layout(
            title=f"Rute Terbaik: {best_result['Method']} (Distance: {best_result['Final Distance']:.2f})",
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            hovermode='closest',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison chart
        st.markdown("---")
        st.subheader("📊 Perbandingan Metode")
        
        fig_compare = go.Figure()
        
        methods_list = results_df['Method'].tolist()
        initial_dists = results_df['Initial Distance'].tolist()
        final_dists = results_df['Final Distance'].tolist()
        
        fig_compare.add_trace(go.Bar(
            name='Initial Distance',
            x=methods_list,
            y=initial_dists,
            marker_color='lightcoral'
        ))
        
        if use_3opt:
            fig_compare.add_trace(go.Bar(
                name='After 3-Opt',
                x=methods_list,
                y=final_dists,
                marker_color='lightgreen'
            ))
        
        fig_compare.update_layout(
            title="Perbandingan Jarak Antar Metode",
            xaxis_title="Metode",
            yaxis_title="Jarak Total",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)

# History section
if st.session_state.results_history:
    st.markdown("---")
    st.subheader("📜 Riwayat Hasil")
    
    with st.expander("Lihat Riwayat Lengkap"):
        for i, history in enumerate(reversed(st.session_state.results_history)):
            st.markdown(f"**Run #{len(st.session_state.results_history) - i}** - {history['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"- Jumlah Kota: {history['num_cities']}")
            st.markdown(f"- Menggunakan 3-Opt: {'Ya' if history['use_3opt'] else 'Tidak'}")
            
            hist_df = pd.DataFrame([
                {k: v for k, v in r.items() if k != 'Tour'}
                for r in history['results']
            ])
            st.dataframe(hist_df, use_container_width=True)
            st.markdown("---")
    
    if st.button("🗑️ Clear History"):
        st.session_state.results_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>TSP Heuristic Optimizer | Built with Streamlit</p>
    <p>Metode: NN, NI, FI, CI, AI + 3-Opt Optimization</p>
</div>
""", unsafe_allow_html=True)