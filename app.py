import streamlit as st
import pandas as pd
from data_processor import load_and_clean_excel, execute_instructions
from gemini_client import query_gemini_api
from visualization import plot_bar, plot_histogram, plot_line

st.set_page_config(page_title="Excel Conversational Assistant")

st.title("Excel Conversational Assistant")

uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = load_and_clean_excel(uploaded_file)
    try:
      st.write("Dataset Preview", df.head())
    except Exception as e:
      st.warning(f"Error displaying table: {e}")
      st.text(df.head().to_string())



    user_query = st.text_input("Ask a question about your data")

    if user_query:
        schema_summary = ", ".join(f"{col} ({str(dtype)})" for col, dtype in zip(df.columns, df.dtypes))
        instructions = query_gemini_api(user_query, schema_summary)

        if instructions.get("error"):
            st.error("Error from Gemini API: " + instructions["error"])
        else:
            result_df = execute_instructions(df, instructions)

            if "visualization" in instructions:
                vis = instructions["visualization"]
                if vis == "bar_chart":
                    plot_bar(result_df, instructions.get("x"), instructions.get("y"))
                elif vis == "histogram":
                    plot_histogram(result_df, instructions.get("column"))
                elif vis == "line_chart":
                    plot_line(result_df, instructions.get("x"), instructions.get("y"))
                else:
                    st.write(result_df)
            else:
                st.write(result_df)
