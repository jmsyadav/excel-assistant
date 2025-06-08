import os
import requests
import json
import re

API_KEY = os.getenv("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = "YOUR_API_KEY"

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def extract_json_from_text(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except:
                pass
        for i in range(len(text), 0, -1):
            try:
                return json.loads(text[:i])
            except:
                continue
    return {"error": "Invalid JSON format"}

def query_gemini_api(user_query, schema_summary):
    prompt = f"""You are a data analyst tool. The uploaded Excel file has columns: {schema_summary}.
Respond ONLY in JSON format with these possible keys:
- "filter": {{"column": str, "operator": ">/</==/!=/>=/<=/in", "value": any}}
- "group_by": [str] 
- "aggregate": {{"column": str, "func": "mean/sum/count/min/max/count_rows"}} OR list of these
- "select_columns": [str]
- "visualization": "bar_chart/histogram/line_chart/pie_chart"
- "x": str, "y": str, "column": str
- "statistical_summary": true
- "error": str

Examples:
User: "Show average income by gender"
Response: {{"group_by": ["gender"], "aggregate": {{"column": "income", "func": "mean"}}, "visualization": "bar_chart", "x": "gender", "y": "income"}}

User: "How many customers under 30?"
Response: {{"filter": {{"column": "age", "operator": "<", "value": 30}}, "aggregate": {{"func": "count_rows"}}}}

Current query: {user_query}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if response.status_code != 200:
            return {"error": f"API Error {response.status_code}: {response.text}"}
        
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