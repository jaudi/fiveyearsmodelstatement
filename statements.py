
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

# Growth Rate Calculations
revenue_growth_rate = [0] + [(revenue[i] / revenue[i-1] - 1) * 100 for i in range(1, years)]
gross_profit_growth_rate = [0] + [(gross_profit[i] / gross_profit[i-1] - 1) * 100 for i in range(1, years)]
ebit_growth_rate = [0] + [(ebit[i] / ebit[i-1] - 1) * 100 for i in range(1, years)]
net_income_growth_rate = [0] + [(net_income[i] / net_income[i-1] - 1) * 100 for i in range(1, years)]

# Ratio Calculations
gross_margin = [(gp / rev) * 100 for gp, rev in zip(gross_profit, revenue)]
operating_margin = [(eb / rev) * 100 for eb, rev in zip(ebit, revenue)]
net_profit_margin = [(ni / rev) * 100 for ni, rev in zip(net_income, revenue)]
return_on_assets = [(ni / a) * 100 for ni, a in zip(net_income, assets)]
return_on_equity = [(ni / eq) * 100 for ni, eq in zip(net_income, equity)]

# Convert lists to Pandas DataFrame for better presentation
years_list = [f"Year {i+1}" for i in range(years)]

income_statement = pd.DataFrame({
    "Year": years_list,
    "Revenue": revenue,
    "Revenue Growth Rate (%)": revenue_growth_rate,
    "COGS": cogs,
    "Gross Profit": gross_profit,
    "Gross Profit Growth Rate (%)": gross_profit_growth_rate,
    "Operating Expenses": opex,
    "EBIT": ebit,
    "EBIT Growth Rate (%)": ebit_growth_rate,
    "Tax": tax,
    "Net Income": net_income,
    "Net Income Growth Rate (%)": net_income_growth_rate
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

ratios = pd.DataFrame({
    "Year": years_list,
    "Gross Margin (%)": gross_margin,
    "Operating Margin (%)": operating_margin,
    "Net Profit Margin (%)": net_profit_margin,
    "Return on Assets (ROA) (%)": return_on_assets,
    "Return on Equity (ROE) (%)": return_on_equity
}).round(2)

# Display Financial Statements and Ratios
st.subheader("Income Statement")
st.write(income_statement)

st.subheader("Cash Flow Statement")
st.write(cash_flow_statement)

st.subheader("Balance Sheet")
st.write(balance_sheet)

st.subheader("Financial Ratios")
st.write(ratios)

st.subheader("Net Cash Flow Over Years")
st.line_chart(cash_flow)

st.info("""
**Disclaimer:**

This financial model is provided for informational purposes only and is intended to serve as a general guide for generating a five-year financial projection based on user-input parameters. The outputs are highly dependent on the assumptions outlined below and should not be considered as financial advice or a definitive forecast of future performance.

### Key Assumptions:
1. **Revenue Growth:** The model assumes a constant annual revenue growth rate, as specified by the user. The default rate is set to 10% per annum.
2. **Initial Revenue:** The starting revenue amount is input by the user, with a default value of $100,000. This amount grows according to the specified revenue growth rate.
3. **Cost of Goods Sold (COGS):** COGS is assumed to be a fixed percentage of revenue, adjustable by the user. The default percentage is set to 40%.
4. **Operating Expenses:** Operating expenses are also assumed to be a fixed percentage of revenue, with a default value of 20%.
5. **Tax Rate:** The tax rate is assumed to be constant throughout the projection period, with a default value of 25%.
6. **Capital Expenditures (Capex):** The annual capital expenditures are assumed to be constant, with a default value of $5,000.
7. **Depreciation & Amortization:** The annual depreciation and amortization are also assumed to be constant, with a default value of $5,000.
8. **Change in Net Working Capital (NWC):** The annual change in net working capital is assumed to be constant, with a default value of $500.
9. **Liabilities:** Liabilities are assumed to be 40% of revenue each year.
10. **Equity:** Equity is calculated as the difference between assets and liabilities.
""")
