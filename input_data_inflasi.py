import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

# Fungsi untuk menghubungkan dan mengambil data dari database
def create_connection():
    connection = mysql.connector.connect(
        host="sql12.freesqldatabase.com",        
        user="sql12741637",          
        password="jTA2tzJ2bc",  
        database="sql12741637"   
    )
    return connection

def get_data(query):
    connection = create_connection()
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Fungsi untuk menyimpan data ke database berdasarkan tabel yang berbeda
def insert_data(table_name, data):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        if table_name == "inflasi":
            sql = '''INSERT INTO inflasi (Waktu, `Inflasi yoy (%)`, `Inflasi mtm (%)`) VALUES (%s, %s, %s)'''
            cursor.execute(sql, data)
        elif table_name == "inflasi_yoy":
            sql = '''INSERT INTO inflasi_yoy (Waktu, `Komoditas yoy`, `Andil yoy (%)`, `Fenomena Berdasarkan Inflasi yoy`) VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, data)
        elif table_name == "inflasi_mtm":
            sql = '''INSERT INTO inflasi_mtm (Waktu, `Komoditas mtm`, `Andil mtm (%)`, `Fenomena Berdasarkan Inflasi mtm`) VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, data)

        connection.commit()
        cursor.close()
        connection.close()
        st.write(f"Data berhasil disimpan ke tabel {table_name}")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat menyimpan data: {e}")


def show():
    st.title("Input Data Inflasi Kota Cirebon")

    # Memilih tabel
    st.subheader("Pilih Tabel untuk Input Data")
    table_choice = st.selectbox("Pilih Tabel", ["inflasi", "inflasi_yoy", "inflasi_mtm"])

    current_year = datetime.now().year

    # Menghasilkan daftar tanggal 1 untuk 12 bulan dalam tahun ini dan tahun berikutnya
    valid_dates = [f"{month}/1/{year}" for year in range(current_year, current_year + 10) for month in range(1, 13)]

    # Memilih tanggal 1 dari daftar yang valid
    selected_date = st.selectbox("Pilih Waktu (Tanggal 1 setiap bulan)", valid_dates)

    # Mengubah format tanggal menjadi "MM/DD/YYYY" dan menyimpannya sebagai string
    date_object = datetime.strptime(selected_date, "%m/%d/%Y")
    waktu = date_object.strftime("%m/%d/%Y")  # Tetap menggunakan format ini untuk disimpan sebagai string

    # Form Input Data Inflasi
    with st.form(key='form_input_inflasi'):
        if table_choice == "inflasi":
            # Input Inflasi YoY (%), bisa negatif
            inflasi_yoy = st.number_input("Inflasi YoY (%)", format="%.2f", key="inflasi_yoy")
            
            # Input Inflasi MtM (%), bisa negatif
            inflasi_mtm = st.number_input("Inflasi MtM (%)", format="%.2f", key="inflasi_mtm")
        
        elif table_choice == "inflasi_yoy":
            st.subheader("10 Komoditas dengan Nilai Inflasi YoY Tertinggi")
            komoditas_inflasi_yoy = []
            for i in range(1, 11):
                komoditas = st.text_input(f"Komoditas Inflasi YoY {i}", key=f"kom_inflasi_yoy_{i}")
                andil_input = st.number_input(f"Andil Komoditas Inflasi YoY {i} (%)", min_value=0.0, format="%.4f", key=f"andil_inflasi_yoy_{i}")
                fenomena = st.text_area(f"Fenomena Komoditas Inflasi YoY {i}", key=f"fenomena_inflasi_yoy_{i}")
                komoditas_inflasi_yoy.append((waktu, komoditas, andil_input, fenomena))

            st.subheader("10 Komoditas dengan Nilai Deflasi YoY Tertinggi")
            komoditas_deflasi_yoy = []
            for i in range(1, 11):
                komoditas = st.text_input(f"Komoditas Deflasi YoY {i}", key=f"kom_deflasi_yoy_{i}")
                andil_input = st.number_input(f"Andil Komoditas Deflasi YoY {i} (%)", max_value=0.0, format="%.4f", key=f"andil_deflasi_yoy_{i}")
                fenomena = st.text_area(f"Fenomena Komoditas Deflasi YoY {i}", key=f"fenomena_deflasi_yoy_{i}")
                komoditas_deflasi_yoy.append((waktu, komoditas, andil_input, fenomena))
        
        elif table_choice == "inflasi_mtm":
            st.subheader("10 Komoditas dengan Nilai Inflasi MtM Tertinggi")
            komoditas_inflasi_mtm = []
            for i in range(1, 11):
                komoditas = st.text_input(f"Komoditas Inflasi MtM {i}", key=f"kom_inflasi_mtm_{i}")
                andil_input = st.number_input(f"Andil Komoditas Inflasi MtM {i} (%)", min_value=0.0, format="%.4f", key=f"andil_inflasi_mtm_{i}")
                fenomena = st.text_area(f"Fenomena Komoditas Inflasi MtM {i}", key=f"fenomena_inflasi_mtm_{i}")
                komoditas_inflasi_mtm.append((waktu, komoditas, andil_input, fenomena))

            st.subheader("10 Komoditas dengan Nilai Deflasi MtM Tertinggi")
            komoditas_deflasi_mtm = []
            for i in range(1, 11):
                komoditas = st.text_input(f"Komoditas Deflasi MtM {i}", key=f"kom_deflasi_mtm_{i}")
                andil_input = st.number_input(f"Andil Komoditas Deflasi MtM {i} (%)", max_value=0.0, format="%.4f", key=f"andil_deflasi_mtm_{i}")
                fenomena = st.text_area(f"Fenomena Komoditas Deflasi MtM {i}", key=f"fenomena_deflasi_mtm_{i}")
                komoditas_deflasi_mtm.append((waktu, komoditas, andil_input, fenomena))
        
        # Tombol Submit
        submit_button = st.form_submit_button(label="Submit Data")

        # Validasi sebelum submit
        if submit_button:
            all_filled = True
            
            # Validasi tergantung pada tabel yang dipilih
            if table_choice == "inflasi":
                if inflasi_yoy is None or inflasi_mtm is None:
                    all_filled = False
                    st.error("Isian untuk Inflasi YoY dan MtM belum lengkap!")
            elif table_choice == "inflasi_yoy":
                for data in komoditas_inflasi_yoy + komoditas_deflasi_yoy:
                    # Pastikan data yang di-unpack sesuai
                    if len(data) != 4 or not data[1] or data[2] is None or not data[3]:
                        all_filled = False
                        st.error("Isian untuk Komoditas Inflasi/Deflasi YoY belum lengkap!")
            elif table_choice == "inflasi_mtm":
                for data in komoditas_inflasi_mtm + komoditas_deflasi_mtm:
                    # Pastikan data yang di-unpack sesuai
                    if len(data) != 4 or not data[1] or data[2] is None or not data[3]:
                        all_filled = False
                        st.error("Isian untuk Komoditas Inflasi/Deflasi MtM belum lengkap!")

            if all_filled:
                # Menyimpan data ke database
                if table_choice == "inflasi":
                    insert_data("inflasi", (waktu, inflasi_yoy, inflasi_mtm))
                elif table_choice == "inflasi_yoy":
                    for data in komoditas_inflasi_yoy + komoditas_deflasi_yoy:
                        insert_data("inflasi_yoy", data)
                elif table_choice == "inflasi_mtm":
                    for data in komoditas_inflasi_mtm + komoditas_deflasi_mtm:
                        insert_data("inflasi_mtm", data)

                st.success("Data berhasil disubmit!")
                st.write(f"Data yang diinput untuk tabel {table_choice} berhasil disimpan.")
            else:
                st.warning("Silakan lengkapi semua data sebelum mengirim.")

if __name__ == "__main__":
    show()
