import requests
import pandas as pd

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
    response = requests.get(url)
    return pd.DataFrame(response.json())  # Return the DataFrame

# Optional: Test the function
if __name__ == "__main__":
    print(fetch_crypto_data().head())