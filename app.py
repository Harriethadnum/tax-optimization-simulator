import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Helper Functions
def calculate_uk_tax(income, deductions, tax_credits):
    # Personal Allowance
    personal_allowance = 12570
    if income > 100000:
        personal_allowance = max(0, 12570 - ((income - 100000) / 2))

    # Taxable Income
    taxable_income = max(0, income - personal_allowance - deductions)

    # Tax Brackets
    brackets = [
        (0, 37700, 0.2),  # Basic Rate: 20%
        (37701, 125140, 0.4),  # Higher Rate: 40%
        (125141, float("inf"), 0.45),  # Additional Rate: 45%
    ]

    # Calculate Tax
    tax = 0
    for lower, upper, rate in brackets:
        if taxable_income > lower:
            taxable_in_bracket = min(taxable_income, upper) - lower
            tax += taxable_in_bracket * rate
        else:
            break

    return max(0, tax - tax_credits)

def calculate_national_insurance(income):
    # NIC Rates (2024/2025)
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * 0.12
    else:
        return ((50270 - 12570) * 0.12) + ((income - 50270) * 0.02)

def dividend_optimization(income, deductions, tax_credits):
    # Dividend income is taxed at a lower rate
    dividend_allowance = 2000  # Dividend Allowance
    dividend_taxable_income = max(0, income - dividend_allowance)

    if dividend_taxable_income <= 50270:
        dividend_tax = dividend_taxable_income * 0.075  # Tax rate on dividends within the basic rate band
    elif dividend_taxable_income <= 150000:
        dividend_tax = dividend_taxable_income * 0.325  # Tax rate on dividends within the higher rate band
    else:
        dividend_tax = dividend_taxable_income * 0.381  # Tax rate on dividends within the additional rate band
    
    total_tax = calculate_uk_tax(income, deductions, tax_credits) + dividend_tax
    return total_tax

def income_splitting_optimization(income, deductions, tax_credits, partner_income=0):
    # Split income between two individuals to reduce tax liability
    total_income = income + partner_income
    partner_tax_credits = tax_credits / 2  # Split the tax credits as well

    return calculate_uk_tax(total_income / 2, deductions / 2, partner_tax_credits)

def inheritance_tax_planning(income, deductions, tax_credits):
    # Example Inheritance Tax Planning: Annual gifting
    annual_gift_allowance = 3000  # Allowance for gifts without inheritance tax implications
    adjusted_income = income - annual_gift_allowance

    # Calculate tax after making use of annual gifting allowance
    return calculate_uk_tax(adjusted_income, deductions, tax_credits)

def rd_tax_relief(income, deductions, tax_credits):
    # R&D Tax Relief: Assume a certain percentage of income is eligible for R&D tax credits
    rd_allowance = 0.15  # Simplified R&D tax relief rate (15% of income)
    rd_deduction = income * rd_allowance
    return calculate_uk_tax(income - rd_deduction, deductions, tax_credits)

def optimize_retirement_contributions(income, deductions, tax_credits):
    pension_contribution_limit = 60000  # Annual allowance
    contribution = min(income * 0.2, pension_contribution_limit)  # Max 20% or limit
    return calculate_uk_tax(income - contribution, deductions, tax_credits)

def charitable_donations_optimization(income, deductions, tax_credits):
    donation = 10000  # Example donation
    gift_aid_bonus = donation * 0.25  # Gift Aid adds 25%
    tax_relief = donation * 0.2  # Additional 20% tax relief
    return calculate_uk_tax(income - gift_aid_bonus, deductions, tax_credits - tax_relief)

# Streamlit Interface
def main():
    st.title("UK Tax Optimization Simulator")

    # Sidebar Input Section
    st.sidebar.header("Enter Your Tax Details")
    income = st.sidebar.number_input("Annual Income (£)", min_value=0, value=50000, step=1000, help="Your total taxable income before any deductions.")
    deductions = st.sidebar.number_input("Deductions (£)", min_value=0, value=0, step=100, help="Total allowable deductions, such as expenses or retirement contributions.")
    tax_credits = st.sidebar.number_input("Tax Credits (£)", min_value=0, value=0, step=100, help="Any tax credits you are eligible for, such as childcare or energy credits.")
    partner_income = st.sidebar.number_input("Partner's Income (£)", min_value=0, value=0, step=1000, help="If applicable, enter your partner's income for income splitting.")

    strategy = st.sidebar.selectbox(
        "Select Optimization Strategy",
        ["None", "Retirement Contributions", "Charitable Donations", "Dividend Optimization", "Income Splitting", "Inheritance Tax Planning", "R&D Tax Relief"],
        key="strategy_selectbox"
    )

    # Validate Input
    if deductions > income:
        st.sidebar.warning("Deductions exceed income. Please check your inputs.")

    # Tax Optimization Logic
    optimized_tax = None
    if strategy == "None":
        optimized_tax = calculate_uk_tax(income, deductions, tax_credits)
    elif strategy == "Retirement Contributions":
        optimized_tax = optimize_retirement_contributions(income, deductions, tax_credits)
    elif strategy == "Charitable Donations":
        optimized_tax = charitable_donations_optimization(income, deductions, tax_credits)
    elif strategy == "Dividend Optimization":
        optimized_tax = dividend_optimization(income, deductions, tax_credits)
    elif strategy == "Income Splitting":
        optimized_tax = income_splitting_optimization(income, deductions, tax_credits, partner_income)
    elif strategy == "Inheritance Tax Planning":
        optimized_tax = inheritance_tax_planning(income, deductions, tax_credits)
    elif strategy == "R&D Tax Relief":
        optimized_tax = rd_tax_relief(income, deductions, tax_credits)

    # National Insurance Calculation
    national_insurance = calculate_national_insurance(income)

    # Display Results
    if optimized_tax is not None:
        total_tax = optimized_tax + national_insurance
        base_tax = calculate_uk_tax(income, deductions, tax_credits) + calculate_national_insurance(income)
        savings = base_tax - total_tax

        st.subheader(f"Your total tax liability (including National Insurance) using '{strategy}' strategy: £{total_tax:,.2f}")
        st.write(f"- Income Tax: £{optimized_tax:,.2f}")
        st.write(f"- National Insurance: £{national_insurance:,.2f}")
        st.write(f"- Total Savings: £{savings:,.2f}")

        with st.expander("View Detailed Calculation Breakdown"):
            personal_allowance = 12570 if income <= 100000 else max(0, 12570 - ((income - 100000) / 2))
            taxable_income = max(0, income - personal_allowance - deductions)
            st.write(f"Personal Allowance: £{personal_allowance:,.2f}")
            st.write(f"Taxable Income: £{taxable_income:,.2f}")
    else:
        st.error("Please select a valid strategy.")

    # Visualization
    st.subheader("Tax Liability Comparison by Strategy")
    strategies = ["None", "Retirement Contributions", "Charitable Donations", "Dividend Optimization", "Income Splitting", "Inheritance Tax Planning", "R&D Tax Relief"]
    tax_liabilities = [
        calculate_uk_tax(income, deductions, tax_credits) + calculate_national_insurance(income),
        optimize_retirement_contributions(income, deductions, tax_credits) + calculate_national_insurance(income),
        charitable_donations_optimization(income, deductions, tax_credits) + calculate_national_insurance(income),
        dividend_optimization(income, deductions, tax_credits) + calculate_national_insurance(income),
        income_splitting_optimization(income, deductions, tax_credits, partner_income) + calculate_national_insurance(income),
        inheritance_tax_planning(income, deductions, tax_credits) + calculate_national_insurance(income),
        rd_tax_relief(income, deductions, tax_credits) + calculate_national_insurance(income)
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(strategies, tax_liabilities, color=['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink'])
    plt.title('Comparison of Tax Liabilities by Strategy')
    plt.xlabel('Optimization Strategy')
    plt.ylabel('Tax Liability (£)')
    plt.xticks(rotation=45, ha='right')
    for i, tax in enumerate(tax_liabilities):
        plt.text(i, tax, f"£{tax:,.2f}", ha='center', va='bottom')
    st.pyplot(plt)

    # Export Results
    st.subheader("Download Your Results")
    results = pd.DataFrame({
        "Strategy": strategies,
        "Tax Liability (£)": tax_liabilities
    })
    st.download_button("Download Results", results.to_csv(index=False), "tax_results.csv", "text/csv")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
