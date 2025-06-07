import matplotlib.pyplot as plt
import streamlit as st

def plot_bar(df, x_col, y_col):
    if x_col not in df.columns or y_col not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} by {x_col}")
    st.pyplot(fig)

def plot_histogram(df, column):
    if column not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=20)
    ax.set_xlabel(column)
    ax.set_title(f"Histogram of {column}")
    st.pyplot(fig)

def plot_line(df, x_col, y_col):
    if x_col not in df.columns or y_col not in df.columns:
        st.write(df)
        return
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} over {x_col}")
    st.pyplot(fig)
