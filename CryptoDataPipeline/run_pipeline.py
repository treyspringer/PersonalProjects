import schedule
import time
import logging
from fetch_data import fetch_crypto_data
from clean_data import clean_data
from store_data import save_to_sqlite

# Configure logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    try:
        logging.info("Pipeline started")
        
        # Fetch → Clean → Store
        raw_data = fetch_crypto_data()
        cleaned_data = clean_data(raw_data)  # Pass the DataFrame here
        save_to_sqlite(cleaned_data)
        
        logging.info("Pipeline finished successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}", exc_info=True)

# Schedule (runs immediately + every 10 seconds for testing)
run_pipeline()  # First run
schedule.every(10).seconds.do(run_pipeline)

if __name__ == "__main__":
    logging.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(1)