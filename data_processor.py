import pandas as pd
import re

def clean_column_names(cols):
    def clean(col):
        col = col.strip().lower()
        col = re.sub(r'\W+', '_', col)
        return col
    return [clean(c) for c in cols]

def fix_arrow_incompatible_columns(df):
    for col in df.columns:
        if df[col].dtype == "object":
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

def execute_instructions(df, instructions):
    if 'filter' in instructions:
        f = instructions['filter']
        col, op, val = f.get('column'), f.get('operator'), f.get('value')
        if col in df.columns:
            if op == '>':
                df = df[df[col] > val]
            elif op == '<':
                df = df[df[col] < val]
            elif op == '==':
                df = df[df[col] == val]
            elif op == '!=':
                df = df[df[col] != val]
    if 'group_by' in instructions and 'aggregate' in instructions:
        group_cols = [c for c in instructions['group_by'] if c in df.columns]
        agg = instructions['aggregate']
        agg_col, func = agg.get('column'), agg.get('func')
        if agg_col in df.columns and group_cols:
            df = df.groupby(group_cols)[agg_col].agg(func).reset_index()
    if 'select_columns' in instructions:
        cols = [c for c in instructions['select_columns'] if c in df.columns]
        if cols:
            df = df[cols]
    return df
