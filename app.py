import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("📚 EduPro Online Learning Dashboard")

# Load Data
users = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Users")
teachers = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Teachers")
courses = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Courses")
transactions = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Transactions")

# Merge
df = transactions.merge(users, on="UserID")
df = df.merge(courses, on="CourseID")
df = df.merge(teachers, on="TeacherID")

df.rename(columns={
    "Age_x": "UserAge",
    "Age_y": "TeacherAge",
    "Gender_x": "UserGender",
    "Gender_y": "TeacherGender"
}, inplace=True)

# KPI Cards
st.subheader("Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Users", len(users))
col2.metric("Teachers", len(teachers))
col3.metric("Courses", len(courses))
col4.metric("Revenue", f"₹{df['Amount'].sum():,.2f}")

# Gender Chart
st.subheader("Revenue by User Gender")

gender_revenue = df.groupby("UserGender")["Amount"].sum()

fig, ax = plt.subplots()
gender_revenue.plot(kind="bar", ax=ax, color=["steelblue", "pink"])
ax.set_xlabel("Gender")
ax.set_ylabel("Revenue")
st.pyplot(fig)

st.subheader("Revenue by Course Category")

category_revenue = df.groupby("CourseCategory")["Amount"].sum()

st.bar_chart(category_revenue)

# Show Data
st.subheader("Merged Dataset")
st.dataframe(df)
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Select Course Category",
    ["All"] + sorted(df["CourseCategory"].unique().tolist())
)

if category != "All":
    df = df[df["CourseCategory"] == category]

    st.subheader("Payment Method Distribution")

payment = df["PaymentMethod"].value_counts()

st.bar_chart(payment)

st.subheader("Top 10 Courses")

top_courses = (
    df.groupby("CourseName")["Amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top_courses)

df["Month"] = pd.to_datetime(df["TransactionDate"]).dt.month_name()

st.subheader("Monthly Revenue")

monthly = df.groupby("Month")["Amount"].sum()

st.line_chart(monthly)

st.subheader("Top 10 Teachers")

top_teachers = (
    df.groupby("TeacherName")["Amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top_teachers)

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="EduPro_Data.csv",
    mime="text/csv"
)