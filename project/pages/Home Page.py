import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector as ms
import essentials as es


connection_records = ms.connect(
    host = "localhost",
    user = "root",
    password = "mysql@123",
    database = "id_1"
)
cursor_records_mysql = connection_records.cursor()

cursor_records_mysql.execute('''Select budget from settings where enrolment_number = "S25CSEU1504"''')
budget = int(cursor_records_mysql.fetchall()[0][0])

st.title("College Finance Dashboard")
st.caption("Track your expenses, analyze trends, and save smarter.")


col1, col2= st.columns(2)


with col1:
    year_selection = st.selectbox(
        "Select The Year",
        (
            2024,
            2025
        ),
         key = "selectbox_1"
    )
    year_selected = st.session_state["selectbox_1"]
    st.write(f"The selected year is: {year_selected}")

tup = ("January", "February", "March", "April", "May",
         "June", "July", "August", "September", "October",
         "November", "December")
with col2:
    month_selection = st.selectbox(
        "Select Month Of The Year",
        tup,
        key = "selectbox_2"
    )
    month_selected = st.session_state["selectbox_2"]
    st.write(f"The selected month is: {month_selected}")

month_numbers = [x for x in range(1, len(tup) + 1)]
month_number_selected = month_numbers[tup.index(month_selected)]
# st.write(month_number_selected)

query = f"select * from expense_records where YEAR(date) = {year_selected} and MONTH(date) = {month_number_selected}"
cursor_records_mysql.execute(query)
all_values_regarding_the_month_and_year = cursor_records_mysql.fetchall()

food_sum = 0
essentials_sum = 0
other_expenses_sum = 0
for day in all_values_regarding_the_month_and_year:
    food_sum += day[2]
    essentials_sum += day[3]
    other_expenses_sum += day[4]
L = [food_sum, essentials_sum, other_expenses_sum]
# st.write(L)
top_category_index = L.index(max(L))
names = ["Food", "Essentials", "Other Expenses"]
# st.write(names[top_category_index])


# st.write(query)
# st.write(all_values_regarding_the_month_and_year)
# st.write(es.totals_sum_w_avg(all_values_regarding_the_month_and_year))

col1, col2, col3, col4 = st.columns(4)


monthly_total = es.totals_sum_w_avg(all_values_regarding_the_month_and_year)[0]
monthly_avg = es.totals_sum_w_avg(all_values_regarding_the_month_and_year)[1]
col1.metric("💰 Total Spent", f"₹{monthly_total}")
col2.metric("📈 Avg Daily", f"₹{monthly_avg}")
col3.metric("🏆 Top Category", f"{names[top_category_index]}")
col4.metric("💵 Budget Left", f"₹{budget-monthly_total}")

try:
    progress = monthly_total/budget
    st.write("Monthly budget used")
    st.progress(progress)
except:
    st.write("You've already spent over your budget, please ensure that you dont expend more.")
st.write("Your monthly expense distribution!")

labels = ["Food", "Essentials", "Other Expenses"]


data = {
    "Category": ["Food", "Essentials", "Other Expenses"],
    "Amount": L
}


try:
    st.dataframe(pd.DataFrame(data))
    fig, ax = plt.subplots()
    ax.pie(L, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures it's a perfect circle
    st.pyplot(fig)
except:
    st.write("Since there's no expense made till now, there's no representation for it.")
remove_all_data_button = st.button("Remove all records")
if remove_all_data_button:
    cursor_records_mysql.execute("Truncate table expense_records")
    cursor_records_mysql.execute("Truncate table expense_records_food")
    cursor_records_mysql.execute("Truncate table expense_records_essentials")
    cursor_records_mysql.execute("Truncate table expense_records_other_expenses")
    st.rerun()

