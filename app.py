import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Smart Personal Finance & Fraud Alert")

uploaded_file = st.file_uploader("Upload your bank statement CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Data Preview", df.head())

    # Add category column
    df['Category'] = 'Other'
    df.loc[df['Description'].str.contains('Uber', case=False, na=False), 'Category'] = 'Transport'
    df.loc[df['Description'].str.contains('Starbucks', case=False, na=False), 'Category'] = 'Food'

    # Flag big spends
    df['is_anomaly'] = 0
    df.loc[df['Amount'] > 1000, 'is_anomaly'] = 1

    st.subheader("📊 Spend by Category")
    category_sum = df.groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots()
    category_sum.plot.pie(ax=ax, autopct='%1.1f%%')
    st.pyplot(fig)

    st.subheader("🚨 Flagged Anomalies")
    st.write(df[df['is_anomaly']==1])

    st.subheader("✅ All Transactions")
    st.write(df)
