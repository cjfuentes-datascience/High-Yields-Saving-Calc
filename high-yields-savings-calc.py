import streamlit as st
from datetime import datetime, timedelta
import calendar

def calculate_monthly_interest(deposit_per_period, annual_yield=0.044, initial_balance=2594):
    today_date = datetime.now()
    end_of_year = datetime(today_date.year, 12, 31)
    payday_weekday = 2  # Assuming payday is Wednesday

    # Calculate next payday
    days_until_next_payday = (payday_weekday - today_date.weekday()) % 7
    if days_until_next_payday == 0:
        days_until_next_payday = 7
    next_payday = today_date + timedelta(days=days_until_next_payday)

    # Calculate remaining pay periods and months
    remaining_weeks_this_year = (end_of_year - next_payday).days / 7
    remaining_pay_periods = remaining_weeks_this_year // 2
    months_remaining = int((end_of_year - today_date).days / 30)  # Approximate months remaining

    # Monthly interest rate
    monthly_interest_rate = annual_yield / 12

    # Initialize balance and monthly interest list
    balance = initial_balance
    monthly_interest_earnings = []

    for month in range(months_remaining):
        # Add deposit at the start of the month for remaining pay periods
        if month < remaining_pay_periods * 2:
            balance += deposit_per_period
        # Calculate interest for the month
        interest_for_month = balance * monthly_interest_rate
        monthly_interest_earnings.append(interest_for_month)
        # Update balance with interest
        balance += interest_for_month

    # Final balance at the end of the year
    final_balance = balance
    return final_balance, monthly_interest_earnings

# Streamlit UI
st.title('End of Year Savings Calculator')

deposit_per_period = st.number_input("Enter your deposit amount per pay period:", value=244)
annual_yield = st.number_input("Select the annual yield of your savings account (as a percentage):", value=4.4) / 100
initial_balance = st.number_input("Enter your current savings balance:", value=2594)

if st.button('Calculate'):
    final_balance, monthly_interest_earnings = calculate_monthly_interest(deposit_per_period, annual_yield, initial_balance)
    st.write(f"Estimated balance by the end of the year: ${final_balance:.2f}")
    
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    st.write("Monthly interest earnings:")
    for i, interest in enumerate(monthly_interest_earnings, start=1):
        # Calculate month name
        month_name = calendar.month_name[(current_month + i - 1) % 12 or 12]  # Correct for zero-index and loop around
        # Display interest with actual month names
        st.write(f"{month_name}: ${interest:.2f}")
