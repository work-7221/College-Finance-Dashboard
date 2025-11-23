import essentials as es
import streamlit as st
import mysql.connector as ms
from functools import reduce


connection = ms.connect(
    host = "localhost",
    user = "root",
    password = "mysql@123",
    database = "id_1"
)
cursor = connection.cursor()
# cursor.execute("SELECT * FROM expense_records_food")
st.title("💰 Add Your Daily Expenses")
date_label = "Enter Date"
date = st.date_input(date_label, key = "date", format="DD/MM/YYYY")
the_date = st.session_state["date"]

container_1 = st.container()
container_2 = st.container()
container_3 = st.container()


col1, col2= st.columns([1, 1.5])
with col1:
    with st.expander("Food"):
        food = ["Tuck shop", "Quench", "Hotspot", "Southern Stories", "Paid mess", "Bistro", "Vending machine"]
        es.checkbox_maker(food)
with col2:    
    st.subheader("Food")
    es.input_field_maker(food)

essentials_ = ["stationary", "Other"]
with col1:
    with st.expander("Essentials"):
        es.checkbox_maker(essentials_)
with col2:
    st.subheader("Essentials")
    es.input_field_maker(essentials_)

online = ["Recharge", "Subscriptions", "Online Purchases"]
with col1:
    with st.expander("Other Expenses"):
        es.checkbox_maker(online)
with col2:
    st.subheader("Other Expenses")
    es.input_field_maker(online)

col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    submit_button = st.button("Submit")

total = 0


# [element for element in food if element in list(D.keys())]
D = {}
another_dict = {
    "food":[],
    "essentials":[],
    "others":[]
}




if submit_button:
    st.write(st.session_state)
    for i in st.session_state:
        if "input" in i:
            D.update({i : st.session_state[i]})
            try:
                total += eval(st.session_state[i])
            except:
               st.error("Enter all the selected fields with valid inputs.")
               break

for element in food:
    if element+" input" in list(D.keys()):
        try:    
            another_dict["food"].append(eval(st.session_state[element+" input"]))
        except:
            pass
    else:
        another_dict["food"].append(0)

for element in essentials_:
    if element+" input" in list(D.keys()):
        try:
            another_dict["essentials"].append(eval(st.session_state[element+" input"]))
        except:
            pass
    else:
        another_dict["essentials"].append(0)

for element in online:
    if element+" input" in list(D.keys()):
        try:
            another_dict["others"].append(eval(st.session_state[element+" input"]))
        except:
            pass
    else:
        another_dict["others"].append(0)



st.write(D)
st.write(another_dict)

months = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December"
}
if submit_button:
    # st.write(f"INSERT INTO expense_records_food(tuck_shop, quench, hotspot, snapeats, paid_mess, bistro, vending_machine) values{tuple(another_dict["food"])};")
    cursor.execute(f"INSERT INTO expense_records_food(tuck_shop, quench, hotspot, snapeats, paid_mess, bistro, vending_machine) values{tuple(another_dict["food"])};")
    cursor.execute(f"INSERT INTO expense_records_essentials(stationary, other) values{tuple(another_dict["essentials"])}")
    cursor.execute(f"INSERT INTO expense_records_other_expenses(recharge, subscriptions, online_purchases) values{tuple(another_dict["others"])}")

    st.write((the_date).month)
    st.write((the_date).year)
    st.write((the_date).year)
    st.write(type(the_date))
    # month_number = eval(date_formatted[1])

    # cursor.execute(f"INSERT INTO expense_records(date, month, essentials, other_expenses, total) values({the_date, months[the_date.month]}, st.session_state[])")
    connection.commit()

    my_sum = lambda x,y: x+y

    try:
        # cursor.execute("select (tuck_shop+quench+hotspot+snapeats+paid_mess+bistro+vending_machine) as row_sum_food from expense_records_food;")
        cursor.execute("select (tuck_shop+quench+hotspot+snapeats+paid_mess+bistro+vending_machine) from expense_records_food order by serial_number DESC limit 1;")
        row_food = (cursor.fetchall())
        food_sum  =(int(reduce(my_sum, [x[0] for x in row_food])))
    except:
        pass

    try:
        cursor.execute("select (stationary + other) from expense_records_essentials order by serial_number DESC limit 1;")
        row_essentials = (cursor.fetchall())
        essentials_sum  =(int(reduce(my_sum, [x[0] for x in row_essentials])))
    except:
        pass

    try:
        cursor.execute("select (recharge+subscriptions+online_purchases) as row_sum_other_expenses from expense_records_other_expenses order by serial_number DESC limit 1;;")
        row_other_expenses = (cursor.fetchall())
        other_expenses_sum  = (int(reduce(my_sum, [x[0] for x in row_other_expenses])))
    except:
        pass

    # cursor.execute(f"insert into expense_records(date,month,food,essentials,other_expenses,total) values({the_date},{the_date.month},{food_sum},{essentials_sum},{other_expenses_sum},{food_sum+essentials_sum+other_expenses_sum});")
    query = """
    INSERT INTO expense_records
    (date, month, food, essentials, other_expenses, total)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = (
        the_date,
        the_date.month,
        food_sum,
        essentials_sum,
        other_expenses_sum,
        food_sum + essentials_sum + other_expenses_sum
    )

    cursor.execute(query, data)
    connection.commit()
    st.write(the_date)
    print(the_date)
    st.write(food_sum)
    st.write(essentials_sum)
    st.write(other_expenses_sum)


if total != 0:
    st.success("Expense saved successfully.")
    st.header(f"Total expenses made on {date}")
    st.subheader(f"₹{total}")
    st.balloons()

    