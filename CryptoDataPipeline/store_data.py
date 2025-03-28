import sqlite3

def save_to_sqlite(df, db_name="data/crypto_data.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("crypto_prices", conn, if_exists="replace", index=False)
    conn.close()

# Optional: Test the function
if __name__ == "__main__":
    import pandas as pd
    test_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    save_to_sqlite(test_df)