import pandas as pd

def reconcile_dataframes(df_a, df_b, key_a, key_b):
    """
    Reconciles two dataframes based on a common key (e.g., Transaction ID).
    Returns a dictionary with matched and unmatched dataframes.
    """
    # Ensure keys are string type for accurate matching
    df_a[key_a] = df_a[key_a].astype(str).str.strip()
    df_b[key_b] = df_b[key_b].astype(str).str.strip()

    # Perform Outer Join
    merged = pd.merge(
        df_a, 
        df_b, 
        left_on=key_a, 
        right_on=key_b, 
        how='outer', 
        indicator=True,
        suffixes=('_A', '_B')
    )

    # Split results
    matched = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])
    unmatched_a = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    unmatched_b = merged[merged['_merge'] == 'right_only'].drop(columns=['_merge'])

    return {
        "matched": matched,
        "unmatched_a": unmatched_a,
        "unmatched_b": unmatched_b,
        "summary": {
            "total_a": len(df_a),
            "total_b": len(df_b),
            "matches": len(matched),
            "missing_in_b": len(unmatched_a),
            "missing_in_a": len(unmatched_b)
        }
    }
