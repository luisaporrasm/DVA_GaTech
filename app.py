import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# Custom CSS to remove padding and margins
st.markdown("""
    <style>
        .css-18e3th9 {
            padding: 0px !important;
        }
        .css-1d391kg {
            padding: 0px !important;
            margin: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def calculate_stress_test_rate(base_rate, buffer=2.0, floor_rate=5.25):
    stress_test_rate = base_rate + buffer
    return max(stress_test_rate, floor_rate)


def calculate_max_home_price(adjusted_monthly_income, annual_interest_rate, amortization_years, downpayment, include_stress_test, base_rate, buffer, floor_rate, property_tax_and_insurance_rate = 0.00657179):
    # Apply stress test if required
    if include_stress_test:
        annual_interest_rate = calculate_stress_test_rate(base_rate, buffer, floor_rate)

    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12 / 100  # converting percentage to decimal
    # Total number of payments
    total_payments = amortization_years * 12
    # Monthly payment for mortgage excluding taxes and insurance
    estimated_taxes_insurance_per_month = adjusted_monthly_income * property_tax_and_insurance_rate / 12 / 100  # converting percentage to decimal
    adjusted_monthly_income = adjusted_monthly_income - estimated_taxes_insurance_per_month 
    # Maximum loan amount calculation
    max_loan_amount = (adjusted_monthly_income * (1 - (1 + monthly_interest_rate) ** -total_payments)) / monthly_interest_rate
    # Estimated home price 
    estimated_home_price = max_loan_amount / (1 - downpayment)  # (1-downpayment) is the loan amount
    
    return estimated_home_price

########################## MORTGAGE CALCULATOR ###############################
col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

with col1:

    st.title('YYCLivingLens')
    #st.text('This is a web app')
    st.markdown('#### **House Affordability Calculator**') 


### INCLUDE STRESS TEST  #####
#### ADD THE INSURANCE IF DOWNPAYMENT IS LESS THAN 20% 

    # User Inputs
    gross_income = st.number_input('Yearly Gross Income', min_value=0.0, value=100000.0, step=1000.0)
    affordability_level = st.select_slider(
        'Affordability Level', 
        options=([i * 0.1 for i in range(0, 6)]),
        value=0.30,   
        label_visibility="visible")
    annual_interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, value=4.0, step=0.1) / 100
    amortization_years = st.number_input('Loan Term in Years', min_value=5, value=30, step=1)
    downpayment = st.select_slider(
        'Down Payment', 
        options=([i * 0.1 for i in range(0,9)]),
        value=0.20,   
        label_visibility="visible")
    
    ####### STRESS TEST #############################
    # New inputs for stress test and insurance calculation
    include_stress_test = st.checkbox('Include Mortgage Stress Test', False)
    if include_stress_test:
        base_rate = st.number_input('Enter the base mortgage rate (%)', min_value=0.0, max_value=100.0, value=5.29, step=0.01)
        buffer = st.number_input('Enter the buffer (%)', min_value=0.0, max_value=100.0, value=2.0, step=0.01)
        floor_rate = st.number_input('Enter the floor rate (%)', min_value=0.0, max_value=100.0, value=5.25, step=0.01)



    ############# OTHER DEBTS #######################
    # Checkbox to include debts
    include_debts = st.checkbox('Include Other Expenses (Debts)', False)

    # Conditional inputs for debts
    if include_debts:
        car_payment = st.number_input('Monthly Car Payment', min_value=0.0, value=0.0, step=50.0)
        credit_card_payment = st.number_input('Monthly Credit Card Payment', min_value=0.0, value=0.0, step=50.0)
        other_loans_payment = st.number_input('Monthly Other Loans Payment', min_value=0.0, value=0.0, step=50.0)
    else:
        car_payment = 0.0
        credit_card_payment = 0.0
        other_loans_payment = 0.0
    
    total_debt_payments = car_payment + credit_card_payment + other_loans_payment if include_debts else 0.0


    if st.button('Calculate Maximum House Price'):
        monthly_gross_income = gross_income /12
        monthly_available_income_house = monthly_gross_income * affordability_level
        adjusted_monthly_income = monthly_available_income_house - total_debt_payments
        max_price = calculate_max_home_price(adjusted_monthly_income, annual_interest_rate, amortization_years, downpayment, include_stress_test, base_rate, buffer, floor_rate, property_tax_and_insurance_rate = 0.00657179)
        st.success(f"The estimated maximum house price you can afford is: ${max_price:,.2f}")
        











