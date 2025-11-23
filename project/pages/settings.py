import streamlit as st
import mysql.connector as ms

connection = ms.connect(
    user = "root",
    password = "mysql@123",
    host = "localhost",
    database = "id_1"
)

cursor = connection.cursor()

cursor.execute("select * from settings")

content = cursor.fetchall()

st.write(content)


name = content[0][0]
college = content[0][1]
enrol = content[0][2]
sql_budget = content[0][3]

st.title("⚙️Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Name: ")
    st.subheader("College: ")
    st.subheader("Enrolment Number: ")
    st.subheader("Budget: ")

settings_expander = st.expander("Budget")

some_var = f"₹{sql_budget} per month"

with settings_expander:
    budget = st.text_input("Enter Budget:", key="budget_input")
    the_budget = st.session_state.get("budget_input", "")

    save = st.button("Save Budget")
    if save:
        if the_budget.isdigit():
            cursor.execute(
                "UPDATE settings SET budget = %s WHERE enrolment_number = %s",
                (int(the_budget), enrol)
            )
            connection.commit()
            some_var = f"₹{the_budget} per month"
            st.success("Budget updated!")
        else:
            st.error("Please enter a valid number.")

with col2:
    st.subheader(f"{name}")
    st.subheader(f"{college}")
    st.subheader(f"{enrol}")
    budget_label = st.subheader(some_var)
