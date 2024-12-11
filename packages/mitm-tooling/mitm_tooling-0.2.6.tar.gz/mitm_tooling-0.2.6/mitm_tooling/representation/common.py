def guess_k(df):
    return sum((1 for c in df.columns if c.startswith('a_') and not c.startswith('a_dt')))
