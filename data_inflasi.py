import streamlit as st
import pandas as pd
import mysql.connector

# Function to connect and fetch data from the database
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

# Function to perform update data
def update_data(query):
    connection = mysql.connector.connect(
        host="sql12.freesqldatabase.com",        
        user="sql12741637",          
        password="jTA2tzJ2bc",  
        database="sql12741637" 
    )
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

# Function to perform delete data
def delete_data(table, row_id):
    query = f"DELETE FROM `{table}` WHERE `id` = {row_id}"
    update_data(query)

# Function to update row in the database
def update_row(table, row_id, updated_row):
    # Add backticks around column names to handle special characters
    set_clause = ', '.join([f"`{col}` = '{val}'" for col, val in updated_row.items()])
    query = f"UPDATE `{table}` SET {set_clause} WHERE `id` = {row_id}"
    update_data(query)

# Function to show data and RUD buttons with pagination
def show():
    st.title("Data Inflasi Kota Cirebon")
    data_option = st.selectbox("Pilih Data:", ["Inflasi", "Andil Inflasi YoY", "Andil Inflasi MtM", "Andil Inflasi YtD"])

    table_name = ""
    if data_option == "Inflasi":
        table_name = "inflasi"
    elif data_option == "Andil Inflasi YoY":
        table_name = "inflasi_yoy"
    elif data_option == "Andil Inflasi MtM":
        table_name = "inflasi_mtm"
    elif data_option == "Andil Inflasi YtD":
        table_name = "inflasi_ytd"

    query = f"SELECT * FROM {table_name}"
    data = get_data(query)

    if 'id' not in data.columns:
        st.error("Kolom 'id' tidak ditemukan dalam tabel. Pastikan tabel memiliki kolom ID yang benar.")
        return

    # Search functionality
    search_term = st.text_input("Cari:", "")
    
    if search_term:
        # Filter the data based on the search term
        data = data[data.astype(str).apply(lambda x: x.str.contains(search_term, case=False).any(), axis=1)]

    # Remove the 'id' column from the displayed data for the editor
    if 'id' in data.columns:
        data_display = data.drop(columns=['id'])  # Drop the 'id' column
    else:
        data_display = data.copy()

    # Pagination settings
    rows_per_page = 20
    total_rows = len(data_display)
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)

    # Dropdown for selecting page number
    selected_page = st.selectbox("Pilih Halaman:", range(1, total_pages + 1) if total_rows > 0 else [1])

    # Calculate the start and end index for the current page
    start_idx = (selected_page - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)  # Ensure we don't exceed total rows
    page_data = data_display.iloc[start_idx:end_idx].copy()

    # Add a sequential number column at the beginning
    page_data.insert(0, 'No.', range(start_idx + 1, end_idx + 1))  # Insert sequential numbers

    # Data editor for editing and deleting
    edited_data = st.data_editor(page_data, 
                                  key="data_editor", 
                                  num_rows="dynamic", 
                                  use_container_width=True)

    # Find changes and update the database
    if edited_data is not None:
        edited_rows = edited_data.to_dict('records')  # Get the edited data as a list of dictionaries

        for idx, updated_row in enumerate(edited_rows):
            original_row = page_data.iloc[idx].to_dict()

            # Compare the edited row with the original row
            if updated_row != original_row:
                # Remove 'No.' column from the update process
                if 'No.' in updated_row:
                    del updated_row['No.']
                
                # Get the corresponding row ID from the original data
                row_id = data.iloc[start_idx + idx]['id']

                # Update the row in the database
                update_row(table_name, row_id, updated_row)
                st.success(f"Data ID {row_id} berhasil diperbarui.")
        
        # Detect if any row is marked for deletion (e.g. a row has been removed from the editor)
        if len(edited_data) < len(page_data):
            for i in range(len(page_data)):
                if i >= len(edited_data):
                    # This row has been deleted, so delete it from the database
                    row_id = data.iloc[start_idx + i]['id']
                    delete_data(table_name, row_id)
                    st.warning(f"Data ID {row_id} berhasil dihapus.")

if __name__ == "__main__":
    show()
