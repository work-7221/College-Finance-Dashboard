import streamlit as st

st.title("⚙️Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Name: ")
    st.subheader("College: ")
    st.subheader("Enrolment Number: ")
    st.subheader("Budget: ")

settings_expander = st.expander("Budget")

some_var = f"₹0 per month"

with settings_expander:
    # st.checkbox("Hello")
    budget = st.text_input("Enter Budget: ",
                           key = "budget input")
    the_budget = st.session_state["budget input"]

    save = st.button("save budget")
    if save:
        some_var = f"₹{the_budget} per month"

with col2:
    st.subheader("Rohan Kumar Maharana")
    st.subheader("Bennett University")
    st.subheader(" S25CSEU1504")
    budget_label = st.subheader(some_var)
