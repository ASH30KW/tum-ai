import streamlit as st
import pandas as pd
from datetime import date

# App title
st.title("🎓 Course Management App")

# Introduction
st.write("Manage your course with ease!")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Dashboard", "Add Course", "View Course"])

# Function to load saved data
def load_data():
    try:
        return pd.read_csv('courses.csv')
    except:
        return pd.DataFrame(columns=["Course Name", "Assignment", "Due Date"])

# Function to save data
def save_data(df):
    df.to_csv('courses.csv', index=False)

# Dashboard Section
if options == "Dashboard":
    st.header("📊 Dashboard")

    # Load the data
    df = load_data()

    # If no data, display message
    if df.empty:
        st.write("No courses available. Add a course to get started.")
    else:
        st.write("### All Courses")
        st.dataframe(df)

# Add Course Section
elif options == "Add Course":
    st.header("📚 Add a New Course")

    # Form to add course details
    with st.form("Add Course Form"):
        course_name = st.text_input("Course Name")
        assignment_name = st.text_input("Assignment")
        due_date = st.date_input("Due Date", date.today())

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Load existing data
            df = load_data()

            # Add new entry
            new_row = {"Course Name": course_name, "Assignment": assignment_name, "Due Date": due_date}
            df = df.append(new_row, ignore_index=True)

            # Save the updated data
            save_data(df)

            st.success("Course added successfully!")

# View Course Section
elif options == "View Course":
    st.header("🔍 View and Manage Courses")

    # Load existing data
    df = load_data()

    if df.empty:
        st.write("No courses to display.")
    else:
        selected_course = st.selectbox("Select a course to view", df["Course Name"].unique())

        course_data = df[df["Course Name"] == selected_course]
        st.write(course_data)

        # Option to delete or update
        if st.button("Delete Course"):
            df = df[df["Course Name"] != selected_course]
            save_data(df)
            st.success("Course deleted successfully!")
            st.experimental_rerun()
