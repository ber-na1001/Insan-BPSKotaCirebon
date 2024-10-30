import streamlit as st
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",        
            user="sql12741637",          
            password="jTA2tzJ2bc",  
            database="sql12741637"  
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def validate_user(username, password):
    """Validate the user against the database and return their role."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM user_insan WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return user[0]  # Return the role
    return None  # Return None if no user found

def show():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        role = validate_user(username, password)
        if role:
            st.session_state.logged_in = True  # Set login state
            st.session_state.user_role = role  # Set user role in session state
            st.success(f"Login successful! Welcome, {role}.")
        else:
            st.error("Invalid username or password")
