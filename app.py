import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

# Load environment variables from .env file
load_dotenv()

# Access environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Check if MONGO_URI is not None
if MONGO_URI is None:
    st.error("MongoDB URI is not set. Please check your .env file.")
else:
    try:
        # Connect to MongoDB with a longer timeout (e.g., 10 seconds)
        client = MongoClient(
            MONGO_URI, serverSelectionTimeoutMS=10000
        )  # 10 seconds timeout
        db = client.student_db
        collection = db.students

        # Streamlit UI
        st.title("Student Management System")

        option = st.sidebar.selectbox(
            "Menu", ["Add Student", "Delete Student", "View Students"]
        )

        if option == "Add Student":
            name = st.text_input("Enter Name:")
            age = st.number_input("Enter Age:", min_value=1, step=1)
            grade = st.text_input("Enter Grade:")
            if st.button("Add"):
                new_student = {"Name": name, "Age": age, "Grade": grade}
                collection.insert_one(new_student)
                st.success("Student added successfully!")

        elif option == "Delete Student":
            name = st.text_input("Enter Name to Delete:")
            if st.button("Delete"):
                collection.delete_one({"Name": name})
                st.success("Student deleted successfully!")

        elif option == "View Students":
            students = list(collection.find())
            if students:
                student_df = pd.DataFrame(students)
                st.table(student_df)
            else:
                st.info("No students found.")

    except ServerSelectionTimeoutError as err:
        st.error(
            f"Error connecting to MongoDB: {err}. Please check your MongoDB connection settings and try again."
        )
    except ConnectionFailure as err:
        st.error(f"Connection failure: {err}. Please check your MongoDB server.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
