import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.signal import argrelextrema
import mysql.connector

# Fungsi untuk menghubungkan dan mengambil data dari database
def get_data(query):
    connection = mysql.connector.connect(
        host="sql12.freesqldatabase.com",        
        user="sql12741637",          
        password="jTA2tzJ2bc",  
        database="sql12741637"    
    )
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Query untuk mengambil data
query_inflasi = "SELECT * FROM inflasi;"
query_yoy = "SELECT * FROM inflasi_yoy;"
query_mtm = "SELECT * FROM inflasi_mtm;"

# Memuat data dari database (langsung dari fungsi tanpa cache)
def load_data():
    data1 = get_data(query_inflasi)
    data2 = get_data(query_yoy)
    data3 = get_data(query_mtm)
    return data1, data2, data3

data1, data2, data3 = load_data()

def show():
    st.title("Visualisasi Inflasi Kota Cirebon")

    # Pastikan kolom 'Waktu' diubah ke tipe datetime
    data1['Waktu'] = pd.to_datetime(data1['Waktu'])
    data2['Waktu'] = pd.to_datetime(data2['Waktu'])
    data3['Waktu'] = pd.to_datetime(data3['Waktu'])
    
    # Membuat filter untuk tahun mulai dari 2021
    filtered_data1 = data1[data1['Waktu'].dt.year >= 2021]
    waktu_options = filtered_data1['Waktu'].dt.strftime('%B %Y').unique()
    selected_waktu = st.selectbox("Pilih Waktu:", options=waktu_options)

    selected_date = pd.to_datetime(selected_waktu)

    # Filter data untuk grafik inflasi YoY
    start_date = selected_date - pd.DateOffset(months=12)
    filtered_inflasi_yoy = data1[(data1['Waktu'] >= start_date) & (data1['Waktu'] <= selected_date)]

    # Grafik Inflasi YoY
    fig_yoy_inflasi = px.line(
        filtered_inflasi_yoy,
        x='Waktu',
        y='Inflasi yoy (%)',
        title=f'Inflasi YoY pada {selected_waktu}',
        labels={'Waktu': 'Waktu', 'Inflasi yoy (%)': 'Inflasi YoY (%)'}
    )

    # Menambahkan anotasi untuk puncak dan lembah
    def find_peaks_and_troughs(y_values):
        y_values = np.array(y_values)
        peaks = argrelextrema(y_values, np.greater)[0]
        troughs = argrelextrema(y_values, np.less)[0]
        return peaks, troughs

    peaks, troughs = find_peaks_and_troughs(filtered_inflasi_yoy['Inflasi yoy (%)'])

    for peak in peaks:
        fig_yoy_inflasi.add_annotation(
            x=filtered_inflasi_yoy['Waktu'].iloc[peak],
            y=filtered_inflasi_yoy['Inflasi yoy (%)'].iloc[peak] + 0.1,
            text=f"{filtered_inflasi_yoy['Inflasi yoy (%)'].iloc[peak]:.2f}%",
            showarrow=False,
            yanchor='top'
        )

    for trough in troughs:
        fig_yoy_inflasi.add_annotation(
            x=filtered_inflasi_yoy['Waktu'].iloc[trough],
            y=filtered_inflasi_yoy['Inflasi yoy (%)'].iloc[trough] - 0.05,
            text=f"{filtered_inflasi_yoy['Inflasi yoy (%)'].iloc[trough]:.2f}%",
            showarrow=False,
            yanchor='top'
        )

    # Menampilkan grafik inflasi YoY
    st.plotly_chart(fig_yoy_inflasi)

    # Grafik Inflasi MtM
    filtered_inflasi_mtm = data1[(data1['Waktu'] >= start_date) & (data1['Waktu'] <= selected_date)]
    fig_mtm_inflasi = px.line(
        filtered_inflasi_mtm,
        x='Waktu',
        y='Inflasi mtm (%)',
        title=f'Inflasi MtM pada {selected_waktu}',
        labels={'Waktu': 'Waktu', 'Inflasi mtm (%)': 'Inflasi MtM (%)'}
    )

    peaks, troughs = find_peaks_and_troughs(filtered_inflasi_mtm['Inflasi mtm (%)'])

    for peak in peaks:
        fig_mtm_inflasi.add_annotation(
            x=filtered_inflasi_mtm['Waktu'].iloc[peak],
            y=filtered_inflasi_mtm['Inflasi mtm (%)'].iloc[peak] + 0.1,
            text=f"{filtered_inflasi_mtm['Inflasi mtm (%)'].iloc[peak]:.2f}%",
            showarrow=False,
            yanchor='top'
        )

    for trough in troughs:
        fig_mtm_inflasi.add_annotation(
            x=filtered_inflasi_mtm['Waktu'].iloc[trough],
            y=filtered_inflasi_mtm['Inflasi mtm (%)'].iloc[trough] - 0.05,
            text=f"{filtered_inflasi_mtm['Inflasi mtm (%)'].iloc[trough]:.2f}%",
            showarrow=False,
            yanchor='top'
        )

    st.plotly_chart(fig_mtm_inflasi)

    # Membuat grafik batang untuk Andil Komoditas YoY
    filtered_df_yoy = data2[data2['Waktu'] == selected_date]
    filtered_df_yoy = filtered_df_yoy.sort_values(by='Andil yoy (%)', ascending=False)
    filtered_df_yoy['Color'] = filtered_df_yoy['Andil yoy (%)'].apply(lambda x: 'blue' if x >= 0 else 'yellow')

    fig_yoy = px.bar(
        filtered_df_yoy,
        x='Andil yoy (%)',
        y='Komoditas yoy',
        text='Andil yoy (%)',
        title=f"Andil Komoditas terhadap Inflasi YoY pada {selected_waktu}",
        labels={'Komoditas': 'Komoditas YoY', 'Andil yoy (%)': 'Andil YoY (%)'},
        orientation='h',
        color='Color',
        color_discrete_map={'blue': 'blue', 'yellow': 'yellow'}
    )

    fig_yoy.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    
    # Update layout to increase chart height
    fig_yoy.update_layout(
        xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1, range=[-0.5, 1.1]),
        yaxis=dict(autorange='reversed'),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        height=550
    )

    st.plotly_chart(fig_yoy)

    # Membuat grafik batang untuk Andil Komoditas MtM
    filtered_df_mtm = data3[data3['Waktu'] == selected_date]
    filtered_df_mtm = filtered_df_mtm.sort_values(by='Andil mtm (%)', ascending=False)
    filtered_df_mtm['Color'] = filtered_df_mtm['Andil mtm (%)'].apply(lambda x: 'blue' if x >= 0 else 'yellow')

    fig_mtm = px.bar(
        filtered_df_mtm,
        x='Andil mtm (%)',
        y='Komoditas mtm',
        text='Andil mtm (%)',
        title=f"Andil Komoditas terhadap Inflasi MtM pada {selected_waktu}",
        labels={'Komoditas': 'Komoditas MtM', 'Andil mtm (%)': 'Andil MtM (%)'},
        orientation='h',
        color='Color',
        color_discrete_map={'blue': 'blue', 'yellow': 'yellow'}
    )

    fig_mtm.update_traces(texttemplate='%{text:.4f}', textposition='outside')

    # Update layout to increase chart height
    fig_mtm.update_layout(
        xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1, range=[-0.5, 0.6]),
        yaxis=dict(autorange='reversed'),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        height=550
    )

    st.plotly_chart(fig_mtm)
