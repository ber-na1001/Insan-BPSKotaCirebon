import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.signal import argrelextrema
import mysql.connector

# Fungsi untuk menghubungkan dan mengambil data dari database
def get_data(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_insan"
    )
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Fungsi untuk menemukan puncak dan lembah
def find_peaks_and_troughs(y_values):
    y_values = np.array(y_values)
    peaks = argrelextrema(y_values, np.greater)[0]
    troughs = argrelextrema(y_values, np.less)[0]
    return peaks, troughs

# Query untuk mengambil data
query_inflasi = "SELECT * FROM inflasi;"
query_yoy = "SELECT * FROM inflasi_yoy;"
query_mtm = "SELECT * FROM inflasi_mtm;"
query_ytd = "SELECT * FROM inflasi_ytd;"

# Memuat data dari database (langsung dari fungsi tanpa cache)
def load_data():
    data1 = get_data(query_inflasi)
    data2 = get_data(query_yoy)
    data3 = get_data(query_mtm)
    data4 = get_data(query_ytd)
    return data1, data2, data3, data4

data1, data2, data3, data4 = load_data()

def show():
    st.title("Visualisasi Inflasi Kota Cirebon")

    # Pastikan kolom 'Waktu' diubah ke tipe datetime
    data1['Waktu'] = pd.to_datetime(data1['Waktu'])
    data2['Waktu'] = pd.to_datetime(data2['Waktu'])
    data3['Waktu'] = pd.to_datetime(data3['Waktu'])
    data4['Waktu'] = pd.to_datetime(data4['Waktu'])

    # Membuat filter untuk tahun mulai dari 2021
    filtered_data1 = data1[data1['Waktu'].dt.year >= 2021]
    waktu_options = filtered_data1['Waktu'].dt.strftime('%B %Y').unique()
    selected_waktu = st.selectbox("Pilih Waktu:", options=waktu_options)

    selected_date = pd.to_datetime(selected_waktu)

    # Definisikan start_date di luar blok if agar tersedia untuk semua opsi
    start_date = selected_date - pd.DateOffset(months=12)

    # Menampilkan pilihan tabel untuk ditampilkan
    tabel_option = st.selectbox("Pilih Tabel Data Inflasi:", ["Inflasi YoY", "Inflasi MtM", "Inflasi YtD"])

    # Menyesuaikan tampilan grafik berdasarkan pilihan tabel
    if tabel_option == "Inflasi YoY":
        # Filter data untuk grafik inflasi YoY
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

        st.plotly_chart(fig_yoy_inflasi)

        # Membuat grafik batang untuk Andil Komoditas YoY
        filtered_df_yoy = data2[data2['Waktu'] == selected_date]
        filtered_df_yoy = filtered_df_yoy.sort_values(by='Andil yoy (%)', ascending=False)
        filtered_df_yoy['Color'] = filtered_df_yoy['Andil yoy (%)'].apply(lambda x: 'dark blue' if x >= 0 else 'orange')

        fig_yoy = px.bar(
            filtered_df_yoy,
            x='Andil yoy (%)',
            y='Komoditas yoy',
            text='Andil yoy (%)',
            title=f"Andil Komoditas terhadap Inflasi YoY pada {selected_waktu}",
            labels={'Komoditas': 'Komoditas YoY', 'Andil yoy (%)': 'Andil YoY (%)'},
            orientation='h',
            color='Color',
            color_discrete_map={'dark blue': 'darkblue', 'orange': 'orange'}
        )

        fig_yoy.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_yoy.update_layout(
            xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1, range=[-0.5, 1.1]),
            yaxis=dict(autorange='reversed'),
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            height=550
        )

        st.plotly_chart(fig_yoy)

        # Tampilkan tabel DataFrame untuk Andil Komoditas YtD dengan nomor
        st.subheader("Tabel Andil Komoditas YoY")
        # Menambahkan kolom nomor
        filtered_df_yoy['No.'] = range(1, len(filtered_df_yoy) + 1)
        # Menampilkan DataFrame dengan kolom nomor di depan
        st.dataframe(filtered_df_yoy[['No.', 'Komoditas yoy', 'Andil yoy (%)', 'Fenomena Berdasarkan Inflasi yoy']], use_container_width=True, hide_index=True)

    elif tabel_option == "Inflasi MtM":
        # Filter data untuk grafik inflasi MtM
        filtered_inflasi_mtm = data1[(data1['Waktu'] >= start_date) & (data1['Waktu'] <= selected_date)]
        fig_mtm_inflasi = px.line(
            filtered_inflasi_mtm,
            x='Waktu',
            y='Inflasi mtm (%)',
            title=f'Inflasi MtM pada {selected_waktu}',
            labels={'Waktu': 'Waktu', 'Inflasi mtm (%)': 'Inflasi MtM (%)'}
        )

        # Menambahkan anotasi untuk puncak dan lembah
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

        # Membuat grafik batang untuk Andil Komoditas MtM
        filtered_df_mtm = data3[data3['Waktu'] == selected_date]
        filtered_df_mtm = filtered_df_mtm.sort_values(by='Andil mtm (%)', ascending=False)
        filtered_df_mtm['Color'] = filtered_df_mtm['Andil mtm (%)'].apply(lambda x: 'dark blue' if x >= 0 else 'orange')

        fig_mtm = px.bar(
            filtered_df_mtm,
            x='Andil mtm (%)',
            y='Komoditas mtm',
            text='Andil mtm (%)',
            title=f"Andil Komoditas terhadap Inflasi MtM pada {selected_waktu}",
            labels={'Komoditas': 'Komoditas MtM', 'Andil mtm (%)': 'Andil MtM (%)'},
            orientation='h',
            color='Color',
            color_discrete_map={'dark blue': 'darkblue', 'orange': 'orange'}
        )

        fig_mtm.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_mtm.update_layout(
            xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1, range=[-0.5, 1.1]),
            yaxis=dict(autorange='reversed'),
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            height=550
        )

        st.plotly_chart(fig_mtm)

        # Tampilkan tabel DataFrame untuk Andil Komoditas YtD dengan nomor
        st.subheader("Tabel Andil Komoditas MtM")
        # Menambahkan kolom nomor
        filtered_df_mtm['No.'] = range(1, len(filtered_df_mtm) + 1)
        # Menampilkan DataFrame dengan kolom nomor di depan
        st.dataframe(filtered_df_mtm[['No.', 'Komoditas mtm', 'Andil mtm (%)', 'Fenomena Berdasarkan Inflasi mtm']], use_container_width=True, hide_index=True)

    elif tabel_option == "Inflasi YtD":
        # Filter data untuk grafik inflasi YtD
        filtered_inflasi_ytd = data1[(data1['Waktu'] >= start_date) & (data1['Waktu'] <= selected_date)]
        fig_ytd_inflasi = px.line(
            filtered_inflasi_ytd,
            x='Waktu',
            y='Inflasi ytd (%)',
            title=f'Inflasi YtD pada {selected_waktu}',
            labels={'Waktu': 'Waktu', 'Inflasi ytd (%)': 'Inflasi YtD (%)'}
        )

        # Menambahkan anotasi untuk puncak dan lembah
        peaks, troughs = find_peaks_and_troughs(filtered_inflasi_ytd['Inflasi ytd (%)'])

        for peak in peaks:
            fig_ytd_inflasi.add_annotation(
                x=filtered_inflasi_ytd['Waktu'].iloc[peak],
                y=filtered_inflasi_ytd['Inflasi ytd (%)'].iloc[peak] + 0.1,
                text=f"{filtered_inflasi_ytd['Inflasi ytd (%)'].iloc[peak]:.2f}%",
                showarrow=False,
                yanchor='top'
            )

        for trough in troughs:
            fig_ytd_inflasi.add_annotation(
                x=filtered_inflasi_ytd['Waktu'].iloc[trough],
                y=filtered_inflasi_ytd['Inflasi ytd (%)'].iloc[trough] - 0.05,
                text=f"{filtered_inflasi_ytd['Inflasi ytd (%)'].iloc[trough]:.2f}%",
                showarrow=False,
                yanchor='top'
            )

        st.plotly_chart(fig_ytd_inflasi)

        # Membuat grafik batang untuk Andil Komoditas YtD
        filtered_df_ytd = data4[data4['Waktu'] == selected_date]
        filtered_df_ytd = filtered_df_ytd.sort_values(by='Andil ytd (%)', ascending=False)
        filtered_df_ytd['Color'] = filtered_df_ytd['Andil ytd (%)'].apply(lambda x: 'dark blue' if x >= 0 else 'orange')

        fig_ytd = px.bar(
            filtered_df_ytd,
            x='Andil ytd (%)',
            y='Komoditas ytd',
            text='Andil ytd (%)',
            title=f"Andil Komoditas terhadap Inflasi YtD pada {selected_waktu}",
            labels={'Komoditas': 'Komoditas YtD', 'Andil ytd (%)': 'Andil YtD (%)'},
            orientation='h',
            color='Color',
            color_discrete_map={'dark blue': 'darkblue', 'orange': 'orange'}
        )

        fig_ytd.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_ytd.update_layout(
            xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1, range=[-0.5, 1.1]),
            yaxis=dict(autorange='reversed'),
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            height=550
        )

        st.plotly_chart(fig_ytd)

        # Tampilkan tabel DataFrame untuk Andil Komoditas YtD dengan nomor
        st.subheader("Tabel Andil Komoditas YtD")
        # Menambahkan kolom nomor
        filtered_df_ytd['No.'] = range(1, len(filtered_df_ytd) + 1)
        # Menampilkan DataFrame dengan kolom nomor di depan
        st.dataframe(filtered_df_ytd[['No.', 'Komoditas ytd', 'Andil ytd (%)', 'Fenomena Berdasarkan Inflasi ytd']], use_container_width=True, hide_index=True)

if __name__ == "__main__":
    show()
