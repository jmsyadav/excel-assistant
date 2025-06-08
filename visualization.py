import matplotlib.pyplot as plt
import streamlit as st

def plot_bar(df, x_col, y_col):
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} by {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_histogram(df, column):
    if df.empty or column not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=20)
    ax.set_xlabel(column)
    ax.set_title(f"Histogram of {column}")
    st.pyplot(fig)

def plot_line(df, x_col, y_col):
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} over {x_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_pie(df, column, value):
    if df.empty or column not in df.columns or value not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.pie(df[value], labels=df[column], autopct='%1.1f%%')
    ax.set_title(f"{value} by {column}")
    st.pyplot(fig)

    