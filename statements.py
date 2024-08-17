
import streamlit as st
import pandas as pd
import numpy as np

# Streamlit App Title
st.title("Five-Year Financial Statements Model")

# Input Parameters Section
st.sidebar.header("Input Parameters")

years = 5
revenue_growth = st.sidebar.slider("Annual Revenue Growth Rate (%)", 0, 100, 10)
initial_revenue = st.sidebar.number_input("Initial Revenue", min_value=0, value=100000)
cogs_percentage = st.sidebar.slider("COGS (% of Revenue)", 0, 100, 40)
opex_percentage = st.sidebar.slider("Operating Expenses (% of Revenue)", 0, 100, 20)
tax_rate = st.sidebar.slider("Tax Rate (%)", 0, 100, 25)
capex = st.sidebar.number_input("Annual Capital Expenditures", min_value=0, value=5000)
dep_amort = st.sidebar.number_input("Annual Depreciation & Amortization", min_value=0, value=5000)
change_in_nwc = st.sidebar.number_input("Annual Change in NWC", value=500)

# Initialize data structures to hold the values for each year
revenue = [initial_revenue]
cogs = []
gross_profit = []
opex = []
ebit = []
tax = []
net_income = []
operating_cash_flow = []
investing_cash_flow = []
cash_flow = []
assets = []
liabilities = []
equity = []

# Loop through each year to calculate the financials
for year in range(years):
    # Revenue calculation for each year
    if year > 0:
        revenue.append(revenue[-1] * (1 + revenue_growth / 100))
    
    # Income Statement Calculations
    cogs.append(revenue[year] * cogs_percentage / 100)
    gross_profit.append(revenue[year] - cogs[year])
    opex.append(revenue[year] * opex_percentage / 100)
    ebit.append(gross_profit[year] - opex[year])
    tax.append(ebit[year] * tax_rate / 100)
    net_income.append(ebit[year] - tax[year])
    
    # Cash Flow Statement Calculations
    operating_cash_flow.append(net_income[year] + dep_amort - change_in_nwc)
    investing_cash_flow.append(-capex)
    cash_flow.append(operating_cash_flow[year] + investing_cash_flow[year])
    
    # Balance Sheet Calculations
    if year == 0:
        assets.append(cash_flow[year] + dep_amort + capex)
    else:
        assets.append(assets[-1] + cash_flow[year] + dep_amort + capex)
    liabilities.append(revenue[year] * 0.4)  # Assume 40% of revenue as liabilities
    equity.append(assets[year] - liabilities[year])

# Convert lists to Pandas DataFrame for better presentation
years_list = [f"Year {i+1}" for i in range(years)]

income_statement = pd.DataFrame({
    "Year": years_list,
    "Revenue": revenue,
    "COGS": cogs,
    "Gross Profit": gross_profit,
    "Operating Expenses": opex,
    "EBIT": ebit,
    "Tax": tax,
    "Net Income": net_income
}).round(2)

cash_flow_statement = pd.DataFrame({
    "Year": years_list,
    "Operating Cash Flow": operating_cash_flow,
    "Investing Cash Flow": investing_cash_flow,
    "Net Cash Flow": cash_flow
}).round(2)

balance_sheet = pd.DataFrame({
    "Year": years_list,
    "Assets": assets,
    "Liabilities": liabilities,
    "Equity": equity
}).round(2)

# Display Financial Statements
st.subheader("Income Statement")
st.write(income_statement)

st.subheader("Cash Flow Statement")
st.write(cash_flow_statement)

st.subheader("Balance Sheet")
st.write(balance_sheet)

st.subheader("Net Cash Flow Over Years")
st.line_chart(cash_flow)
st.info("""
**Disclaimer:**

This financial model is provided for informational purposes only and is intended to serve as a general guide for generating a five-year financial projection based on user-input parameters. The outputs are highly dependent on the assumptions outlined below and should not be considered as financial advice or a definitive forecast of future performance.

### Key Assumptions:
1. **Revenue Growth:** The model assumes a constant annual revenue growth rate, as specified by the user. The default rate is set to 10% per annum.
2. **Initial Revenue:** The starting revenue amount is input by the user, with a default value of $100,000. This amount grows according to the specified revenue growth rate.
3. **Cost of Goods Sold (COGS):** COGS is assumed to be a fixed percentage of revenue, adjustable by the user. The default percentage is set to 40%.
4. **Operating Expenses (OPEX):** Operating expenses are also assumed to be a fixed percentage of revenue. The default setting is 20%.
5. **Tax Rate:** The tax rate applied to EBIT (Earnings Before Interest and Taxes) is user-defined, with a default rate of 25%.
6. **Capital Expenditures (CAPEX):** The model assumes a constant annual capital expenditure amount, input by the user. The default value is $5,000 per year.
7. **Depreciation and Amortization:** The model includes a constant annual depreciation and amortization expense, with a default value of $5,000.
8. **Net Working Capital (NWC):** The change in net working capital is assumed to be constant each year, with a default value of $500.
9. **Liabilities:** Liabilities are assumed to be 40% of revenue each year, a static assumption embedded in the model.
10. **Equity:** Equity is calculated as the difference between assets and liabilities, with assets accruing based on the cash flow, depreciation, and capital expenditures.

### General Notes:
- **Static Assumptions:** Many of the variables are assumed to be constant over the five-year period, which may not reflect the real-world variability of these factors.
- **Simplified Calculations:** This model uses simplified formulas and may omit more complex elements of financial modeling, such as financing, interest, dividends, or variations in tax laws.
- **User Responsibility:** Users are responsible for inputting accurate data and for understanding the implications of these assumptions on the generated financial statements.

The outputs of this model should be reviewed with caution and should not be used as the sole basis for financial decisions. For comprehensive financial planning, consultation with a financial advisor or accountant is recommended.
""")