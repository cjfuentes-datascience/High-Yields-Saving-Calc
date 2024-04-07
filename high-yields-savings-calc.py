import streamlit as st
from datetime import datetime, timedelta

def calculate_end_of_year_balance(deposit_per_period, annual_yield=0.044, initial_balance=2594):
    today_date = datetime.now()
    end_of_year = datetime(today_date.year, 12, 31)
    payday_weekday = 2  # Assuming payday is Wednesday

    # Calculate next payday
    days_until_next_payday = (payday_weekday - today_date.weekday()) % 7
    if days_until_next_payday == 0:
        days_until_next_payday = 7
    next_payday = today_date + timedelta(days=days_until_next_payday)

    # Calculate remaining pay periods
    remaining_weeks_this_year = (end_of_year - next_payday).days / 7
    remaining_pay_periods = remaining_weeks_this_year // 2

    # Adjust total deposits for the remaining pay periods
    adjusted_total_deposits = deposit_per_period * remaining_pay_periods

    # Adjusted new balance before interest
    new_balance_before_interest_adjusted = initial_balance + adjusted_total_deposits

    # Adjusted interest for the remaining months
    months_remaining = (end_of_year - today_date).days / 30  # Approximate months remaining
    adjusted_annual_yield = annual_yield * (months_remaining / 12)
    adjusted_interest_earned = new_balance_before_interest_adjusted * adjusted_annual_yield

    # Final adjusted balance
    adjusted_final_balance = new_balance_before_interest_adjusted + adjusted_interest_earned
    return adjusted_final_balance

# Streamlit UI
st.title('End of Year Savings Calculator')

deposit_per_period = st.number_input("Enter your deposit amount per pay period:", value=244)
# Updated to use a slider for annual yield
annual_yield = st.slider("Select the annual yield of your savings account (as a percentage):", min_value=0.0, max_value=10.0, value=4.4) / 100
initial_balance = st.number_input("Enter your current savings balance:", value=2594)

if st.button('Calculate'):
    result = calculate_end_of_year_balance(deposit_per_period, annual_yield, initial_balance)
    st.write(f"Estimated balance by the end of the year: ${result:.2f}")
