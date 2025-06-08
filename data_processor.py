import pandas as pd
import re

def clean_column_names(cols):
    return [re.sub(r'[\W\s]+', '_', c.strip().lower()) for c in cols]

def fix_arrow_incompatible_columns(df):
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col], errors="ignore")
            except:
                pass
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except:
                df[col] = df[col].astype(str)
    return df

def load_and_clean_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df.columns = clean_column_names(df.columns)
    df = fix_arrow_incompatible_columns(df)
    return df

def generate_statistical_summary(df, column):
    if column not in df.columns:
        return "Column not found"
    stats = {
        "mean": df[column].mean(),
        "median": df[column].median(),
        "min": df[column].min(),
        "max": df[column].max(),
        "std": df[column].std(),
        "count": df[column].count()
    }
    return stats

def execute_instructions(df, instructions):
    if 'filter' in instructions:
        f = instructions['filter']
        if isinstance(f, dict):
            col, op, val = f.get('column'), f.get('operator'), f.get('value')
            if col in df.columns and op in [">", "<", "==", "!=", ">=", "<=", "in"]:
                if op == '>':
                    df = df[df[col] > val]
                elif op == '<':
                    df = df[df[col] < val]
                elif op == '==':
                    df = df[df[col] == val]
                elif op == '!=':
                    df = df[df[col] != val]
                elif op == '>=':
                    df = df[df[col] >= val]
                elif op == '<=':
                    df = df[df[col] <= val]
                elif op == 'in':
                    df = df[df[col].isin(val)]
    
    if 'group_by' in instructions and 'aggregate' in instructions:
        group_cols = [c for c in instructions['group_by'] if c in df.columns]
        agg_dict = {}
        
        if isinstance(instructions['aggregate'], list):
            for a in instructions['aggregate']:
                if isinstance(a, dict) and a.get('column') in df.columns:
                    agg_dict[a['column']] = a.get('func')
        elif isinstance(instructions['aggregate'], dict):
            a = instructions['aggregate']
            if a.get('column') in df.columns:
                agg_dict[a['column']] = a.get('func')
        
        if agg_dict and group_cols:
            try:
                if "count_rows" in agg_dict.values():
                    result = df.groupby(group_cols, dropna=False).size().reset_index(name='count')
                    return result
                else:
                    df = df.groupby(group_cols, dropna=False).agg(agg_dict)
                    df.columns = ['_'.join(col).strip() for col in df.columns.values]
                    return df.reset_index()
            except Exception as e:
                return pd.DataFrame({"error": [f"Aggregation failed: {e}"]})
    
    if 'select_columns' in instructions:
        cols = [c for c in instructions['select_columns'] if c in df.columns]
        if cols:
            df = df[cols]
    
    return df