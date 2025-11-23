import streamlit as st
def input_field_maker(array, function_key = " input"):
    for i in array:
        if st.session_state[i + " checkbox"]:
            st.text_input(i, key = i + function_key)

def checkbox_maker(array, function_key = " checkbox"):
    for i in array:
        label = i
        checkbox = st.checkbox(label, key = (i + function_key))

    return checkbox

def dictionary_maker(list_of_tuples):
    D = {}
    for i in list_of_tuples:
        D.update({i[0] : i[1]})
    
    return D

def totals_sum_w_avg(array):
    print(array)
    sum = 0
    for x in array:
        sum += x[5]
    try:
        average = sum/len(array)
    except:
        average = 0

    return (sum, average)