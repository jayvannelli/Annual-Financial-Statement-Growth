import requests

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

FMP_BASE_URL = "https://financialmodelingprep.com/api/v3/"

def get_income_statement_growth(symbol, limit, return_df):
    req_url = FMP_BASE_URL + f"income-statement-growth/{symbol.upper()}?limit={limit}&apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()

    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req

    return df

def get_balance_sheet_growth(symbol, limit, return_df):
    req_url = FMP_BASE_URL + f"balance-sheet-statement-growth/{symbol.upper()}?limit={limit}&apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()

    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req

    return df

def get_cash_flow_growth(symbol, limit, return_df):
    req_url = FMP_BASE_URL + f"cash-flow-statement-growth/{symbol.upper()}?limit={limit}&apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()

    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req

    return df

def plot_statements(df, included_data):
    df.plot(x='date', y=included_data, kind='bar').invert_xaxis()
    st.pyplot(plt)

st.header("Annual Financial Statement Growth Dashboard - Justin Vannelli")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Ticker: ")
with col2:
    financial_statement = st.selectbox("Financial Statement", ["Income Statement", "Balance Sheet", "Cash Flow"])
with col3:
    last_x_reports = st.selectbox("Last ___ reports: ", [5,10,15,20])

if ticker:
    st.write('---')

    income_statement_growth = get_income_statement_growth(symbol=ticker, limit=last_x_reports, return_df=True)
    balance_sheet_growth = get_balance_sheet_growth(symbol=ticker, limit=last_x_reports, return_df=True)
    cash_flow_growth = get_cash_flow_growth(symbol=ticker, limit=last_x_reports, return_df=True)

    if financial_statement == "Income Statement":
        income_statement_columns = income_statement_growth.columns[3:]
        income_statement_selections = st.multiselect("Choose which metrics to display", income_statement_columns)

        if income_statement_selections:
            plot_statements(income_statement_growth, income_statement_selections)

        st.write(income_statement_growth)

    elif financial_statement == "Balance Sheet":
        balance_sheet_columns = balance_sheet_growth.columns[3:]
        balance_sheet_selections = st.multiselect("Choose which metrics to display", balance_sheet_columns)

        if balance_sheet_selections:
            plot_statements(balance_sheet_growth, balance_sheet_selections)

        st.write(balance_sheet_growth)

    else:
        cash_flow_columns = cash_flow_growth.columns[3:]
        cash_flow_selections = st.multiselect("Choose which metrics to display", cash_flow_columns)

        if cash_flow_selections:
            plot_statements(cash_flow_growth, cash_flow_selections)

        st.write(cash_flow_growth)