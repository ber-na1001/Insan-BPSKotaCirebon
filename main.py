import streamlit as st
from streamlit import option_menu
import tentang_inflasi
import input_data_inflasi
import data_inflasi
import visualisasi_inflasi
import data_lengkap_inflasi
import login

st.set_page_config(
    page_title="INSAN BPS Kota Cirebon",
    page_icon="Logo BPS.png",
    layout="wide" 
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Create a sidebar with option menu
with st.sidebar: 
    st.markdown("""
        <div style="margin-top: -20px">
            <img src="Logo BPS.png" width="40" style="margin-right: 10px; vertical-align: middle;">
            <h1 style="display: inline; vertical-align: middle;">INSAN</h1>
            <p style="font-size: 14px; color: gray; margin-bottom: 10px;">Indikator Strategis BPS Kota Cirebon</p>
        </div>
    """, unsafe_allow_html=True)


    # Display menu options based on login status
    if not st.session_state.logged_in:
        selected = option_menu(
            "",
            ["Login", "Tentang Inflasi", "Visualisasi Inflasi", "Data Lengkap Inflasi"],
            default_index=0
        )
    else:
        # Show options based on user role
        if st.session_state.user_role == "admin":
            selected = option_menu(
                "",
                ["Tentang Inflasi", "Input Data Inflasi", "Data Inflasi", "Visualisasi Inflasi", "Data Lengkap Inflasi", "Logout"],
                default_index=0
            )
        elif st.session_state.user_role == "tamu":
            selected = option_menu(
                "",
                ["Tentang Inflasi", "Visualisasi Inflasi", "Data Lengkap Inflasi", "Logout"],
                default_index=0
            )

# Handle the Login menu
if selected == "Login":
    login.show()

# Check if the user is logged in
if st.session_state.logged_in:
    # Menu "Tentang Inflasi"
    if selected == "Tentang Inflasi":
        tentang_inflasi.show()

    # Menu "Input Data Inflasi" (only for admin)
    if selected == "Input Data Inflasi" and st.session_state.user_role == "admin":
        input_data_inflasi.show()

    # Menu "Data Inflasi" (only for admin)
    if selected == "Data Inflasi" and st.session_state.user_role == "admin":
        data_inflasi.show()

    # Menu "Visualisasi Inflasi"
    if selected == "Visualisasi Inflasi":
        visualisasi_inflasi.show()

    # Menu "Data Lengkap Inflasi"
    if selected == "Data Lengkap Inflasi":
        data_lengkap_inflasi.show()
    
    # Handle Logout
    if selected == "Logout":
        # Confirmation dialog
        if st.button("Konfirmasi Logout"):
            st.session_state.logged_in = False  # Clear the login state
            st.session_state.user_role = None  # Clear the user role
            st.success("Anda telah keluar.")
        else:
            st.warning("Apakah Anda yakin ingin keluar? Klik 'Konfirmasi Logout' untuk melanjutkan.")
else:
    st.warning("Silakan masuk untuk mengakses aplikasi.")
