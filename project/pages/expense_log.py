import mysql.connector as ms
import streamlit as st
import matplotlib.pyplot as plt
connection = ms.connect(
    host="localhost",
    user="root",
    password="mysql@123",
    database="id_1"
)
cursor = connection.cursor()

st.title("📘 Expense Log")
st.write("View all your expenses for a selected date.")
st.markdown("---")


selected_date = st.date_input("Select Date to View Expenses")

cursor.execute(
    # "SELECT food, essentials, other_expenses, total FROM expense_records WHERE date = %s",
    "select sum(food), sum(essentials), sum(other_expenses), sum(total) from expense_records where date = %s",
    (str(selected_date),)
)
result = cursor.fetchone()
# st.write(selected_date)

if result is None:
    st.info("No expenses recorded for this date.")
else:
    food, essentials, other_expenses, total = result

    st.subheader(f"Expenses on {selected_date.strftime('%d %B, %Y')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🍽 Food", f"₹{food}")

    with col2:
        st.metric("🛍 Essentials", f"₹{essentials}")

    with col3:
        st.metric("📦 Other Expenses", f"₹{other_expenses}")

    st.markdown("---")
    st.metric("💵 Total Spent", f"₹{total}")

    # Simple pie chart
    try:
    
        labels = ["Food", "Essentials", "Other"]
        values = [food, essentials, other_expenses]
    
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)
    except:
        pass
