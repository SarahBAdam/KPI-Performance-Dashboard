# app.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Sales Optimization Dashboard", layout="wide")

st.title("Business Sales Optimization Dashboard")

# Connect to SQLite DB (for demo purposes)
conn = sqlite3.connect('sales.db')
c = conn.cursor()

# Check if table exists, if not create and insert sample data
c.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_name TEXT,
    region TEXT,
    sale_date TEXT,
    quantity INTEGER,
    unit_price REAL
)
""")
conn.commit()

# Insert sample data (optional: comment out after first run to avoid duplicates)
sample_data = [
    (1, 'Product A', 'Gauteng', '2025-01-10', 10, 150.00),
    (2, 'Product B', 'KZN', '2025-01-12', 5, 300.00),
    (3, 'Product A', 'Western Cape', '2025-02-01', 8, 150.00),
    (4, 'Product C', 'Gauteng', '2025-02-05', 15, 120.00)
]
c.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?,?)", sample_data)
conn.commit()

# Load data into pandas
df = pd.read_sql_query("SELECT * FROM sales", conn)
df['sale_date'] = pd.to_datetime(df['sale_date'])

# KPI: Total Revenue
df['total'] = df['quantity'] * df['unit_price']
total_revenue = df['total'].sum()
st.metric("Total Revenue", f"R{total_revenue:,.2f}")

# KPI: Total Units Sold
total_units = df['quantity'].sum()
st.metric("Total Units Sold", total_units)

# Revenue Trend
st.subheader("Revenue Trend by Month")
revenue_month = df.groupby(df['sale_date'].dt.to_period("M")).sum().reset_index()
revenue_month['sale_date'] = revenue_month['sale_date'].dt.to_timestamp()
st.line_chart(revenue_month.set_index('sale_date')['total'])

#
