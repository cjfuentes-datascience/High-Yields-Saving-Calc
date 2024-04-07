import streamlit as st
from datetime import datetime, timedelta
import calendar

def calculate_monthly_interest(deposit_per_period, annual_yield=0.044, initial_balance=2594):
    today_date = datetime.now()
    end_of_year = datetime(today_date.year, 12, 31)
    payday_weekday = 2  # Assuming payday is Wednesday

    # Calculate next payday
    days_until_next_payday = (payday_weekday - today_date.weekday()) % 7
    if days_until_next_payday == 0: # If today is payday, consider the next payday to be in the next pay cycle
        days_until_next_payday = 7
    next_payday = today_date + timedelta(days=days_until_next_payday)

    # Estimate the number of paydays left in the year by considering the weeks until the year's end from the next payday
    weeks_until_end_of_year = (end_of_year - next_payday).days / 7
    pay_periods_remaining = int(weeks_until_end_of_year // 2)  # Paydays occur every two weeks

    # Initialize balance and monthly interest list
    balance = initial_balance
    monthly_interest_earnings = []
    monthly_deposit = deposit_per_period * 2  # Assuming two pay periods per month

    for _ in range(today_date.month, 13):  # Loop from current month to December
        if pay_periods_remaining > 0:
            balance += monthly_deposit  # Add monthly deposit assuming two pay periods per month
            pay_periods_remaining -= 2  # Two pay periods accounted for

        # Calculate monthly interest
        monthly_interest = balance * (annual_yield / 12)
        monthly_interest_earnings.append(monthly_interest)
        
        # Update balance with monthly interest
        balance += monthly_interest

    final_balance = balance
    return final_balance, monthly_interest_earnings

# Streamlit UI
st.title('End of Year Savings Calculator')

deposit_per_period = st.number_input("Enter your deposit amount per pay period:", value=244)
annual_yield = st.slider("Select the annual yield of your savings account (as a percentage):", min_value=0.0, max_value=10.0, value=4.4) / 100
initial_balance = st.number_input("Enter your current savings balance:", value=2594)

if st.button('Calculate'):
    final_balance, monthly_interest_earnings = calculate_monthly_interest(deposit_per_period, annual_yield, initial_balance)
    st.write(f"Estimated balance by the end of the year: ${final_balance:.2f}")

    current_date = datetime.now()
    monthly_display = ""
    for i, interest in enumerate(monthly_interest_earnings, start=current_date.month):
        month_name = calendar.month_name[i]
        monthly_display += f"* {month_name}: ${interest:.2f}\n"
    # Display bullet points using Markdown
    st.markdown("Monthly interest earnings:")
    st.markdown(monthly_display)
