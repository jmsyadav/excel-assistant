import streamlit as st
import pandas as pd
from data_processor import load_and_clean_excel, execute_instructions, generate_statistical_summary
from gemini_client import query_gemini_api
from visualization import plot_bar, plot_histogram, plot_line, plot_pie

st.set_page_config(page_title="Excel Conversational Assistant", layout="wide")
st.title("Excel Conversational Assistant")

uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File size exceeds 10MB limit")
        st.stop()
    
    try:
        df = load_and_clean_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.stop()
    
    st.write("Dataset Preview", df.head())
    user_query = st.text_input("Ask a question about your data", key="query_input")
    
    if user_query:
        schema_summary = ", ".join(f"{col} ({str(dtype)})" for col, dtype in zip(df.columns, df.dtypes))
        instructions = query_gemini_api(user_query, schema_summary)
        
        if "error" in instructions:
            st.error("Gemini API Error: " + instructions["error"])
        else:
            if instructions.get("statistical_summary"):
                col = instructions.get("column")
                stats = generate_statistical_summary(df, col)
                if isinstance(stats, dict):
                    st.subheader(f"Statistical Summary for {col}")
                    for k, v in stats.items():
                        st.text(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")
                else:
                    st.text(stats)
            else:
                result_df = execute_instructions(df, instructions)
                
                if "visualization" in instructions:
                    vis_mapping = {
                        "bar_chart": plot_bar,
                        "histogram": plot_histogram,
                        "line_chart": plot_line,
                        "pie_chart": plot_pie
                    }
                    vis_type = instructions["visualization"]
                    
                    if vis_type in vis_mapping:
                        if vis_type == "pie_chart":
                            plot_pie(
                                result_df, 
                                instructions.get("column"), 
                                instructions.get("value")
                            )
                        elif vis_type == "histogram":
                            plot_histogram(
                                result_df, 
                                instructions.get("column")
                            )
                        else:
                            vis_mapping[vis_type](
                                result_df, 
                                instructions.get("x"), 
                                instructions.get("y")
                            )
                    else:
                        st.write(result_df)
                else:
                    st.write(result_df)

                    