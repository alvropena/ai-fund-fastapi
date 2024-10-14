from apscheduler.schedulers.background import BackgroundScheduler
from data_fetcher import get_income_statements

def fetch_and_store_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL']  # Extend as needed
    for ticker in tickers:
        data = get_income_statements(ticker)
        # Implement logic to store data in the database

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_data, 'interval', hours=24)
    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
