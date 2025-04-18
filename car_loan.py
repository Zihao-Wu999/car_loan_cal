import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math


st.title("Car Loan Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
car_value = col1.number_input("Car Price", min_value=0, value=300000)
down_payment_percentage = col1.slider("Down Payment (%)", min_value=0, max_value=70, value=30)
interest_rate = col2.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (years)", min_value=1, max_value=5, value=3)


# Calculate the repayments
deposit = car_value * (down_payment_percentage / 100)
loan_amount = car_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Payment Information")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Down Payment", value=f"${deposit:,.0f}")
col2.metric(label="Monthly Payment", value=f"${monthly_payment:,.2f}")
col3.metric(label="Total Payment", value=f"${total_payments:,.0f}")
col4.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a data-frame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)