import streamlit as st
import pandas as pd
import json

# Initialize session state variables
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []  # Store selected columns
if 'dataset' not in st.session_state:
    st.session_state.dataset = None  # Store the dataset

def display_upload_page():
    # File uploader widget for JSON file
    st.title("ArgillaLabeler")
    uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])

    if uploaded_file is not None:
        try:
            # Load JSON data from uploaded file
            data = json.load(uploaded_file)

            # Flatten nested JSON (if needed) and create DataFrame
            df = pd.json_normalize(data, sep='_')
            st.session_state.dataset = df  # Save the dataset in session state

            # Display the DataFrame
            st.markdown("**Here is the dataset you uploaded:**")
            st.dataframe(df.head(3))  # Display first 3 rows as a preview

            # Generate checkboxes for each column
            st.session_state.selected_columns = []
            st.markdown("**Please select at least one column to display.**")
            for column in df.columns:
                if st.checkbox(column, key=column):
                    st.session_state.selected_columns.append(column)

            # Show "Next" button to navigate to the next page
            if st.button("Next"):
                if st.session_state.selected_columns:
                    st.session_state.page = 2  # Move to the next page
                else:
                    st.warning("Please select at least one column before proceeding.")

        except json.JSONDecodeError:
            st.error("The file is not a valid JSON file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
