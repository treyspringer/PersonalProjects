import pandas as pd

def clean_data(df):  # Accept DataFrame as input
    # Keep only relevant columns
    columns = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'price_change_percentage_24h']
    df = df[columns]
    
    # Rename columns
    df = df.rename(columns={'price_change_percentage_24h': '24h_change'})
    
    # Drop missing values
    return df.dropna()

# Optional: Test the function (requires manual input)
if __name__ == "__main__":
    test_df = pd.DataFrame({
        'id': ['bitcoin', 'ethereum'],
        'current_price': [50000, 3000],
        'market_cap': [1e12, 5e11],
        'price_change_percentage_24h': [5.2, -1.3]
    })
    print(clean_data(test_df))