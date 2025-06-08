import requests
import json
import re
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def extract_json_from_text(text):
    try:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            return {"error": "Gemini response does not contain valid JSON."}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse Gemini response JSON: {str(e)}", "raw_response": text}

def query_gemini_api(user_query, schema_summary):
    prompt = f"""You are a data analyst tool. The uploaded Excel file has the following schema: {schema_summary}.
User query: {user_query}
Return a structured JSON object with any of the keys (if applicable): filter, group_by, aggregate, visualization, x, y, column, select_columns.
If you can't understand or it's not relevant, return: {{ "error": "Reason here" }}"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            return {"error": "No candidates in Gemini response."}

        content = candidates[0].get("content", {}).get("parts", [])
        if not content or "text" not in content[0]:
            return {"error": "Unexpected Gemini response format."}

        text_output = content[0]["text"].strip()
        return extract_json_from_text(text_output)

    except Exception as e:
        return {"error": str(e)}
