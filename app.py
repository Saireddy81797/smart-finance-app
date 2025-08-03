import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Smart Personal Finance & Fraud Alert")

uploaded_file = st.file_uploader("Upload your bank statement CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Show first few rows so you see what's inside
    st.subheader("📄 Data Preview:")
    st.write(df.head())
    
    # Show column names so you know what columns are there
    st.subheader("📝 Columns in your file:")
    st.write(list(df.columns))
    
    # Add category column
    df['Category'] = 'Other'
    df['is_anomaly'] = 0
    
    # Try to categorize based on first text column found
    text_columns = df.select_dtypes(include='object').columns
    if len(text_columns) > 0:
        text_col = text_columns[0]
        st.write(f"ℹ Using column '{text_col}' to categorize")
        
        df.loc[df[text_col].str.contains('Uber', case=False, na=False), 'Category'] = 'Transport'
        df.loc[df[text_col].str.contains('Starbucks', case=False, na=False), 'Category'] = 'Food'
    else:
        st.write("⚠ No text column found to categorize transactions.")
    
    # Flag big spends > 1000
    if 'Amount' in df.columns:
        df.loc[df['Amount'] > 1000, 'is_anomaly'] = 1
    else:
        st.write("⚠ 'Amount' column not found, can't detect anomalies.")

    # Pie chart of spend by category
    st.subheader("📊 Spend by Category")
    category_sum = df.groupby('Category')['Amount'].sum() if 'Amount' in df.columns else None
    
    if category_sum is not None and not category_sum.empty:
        fig, ax = plt.subplots()
        category_sum.plot.pie(ax=ax, autopct='%1.1f%%')
        st.pyplot(fig)
    else:
        st.write("⚠ Cannot create chart – check your CSV has 'Amount' column.")

    # Show anomalies
    st.subheader("🚨 Flagged Anomalies")
    st.write(df[df['is_anomaly']==1])

    # Show all data
    st.subheader("✅ All Transactions")
    st.write(df)
else:
    st.info("📌 Please upload a CSV file to start.")
