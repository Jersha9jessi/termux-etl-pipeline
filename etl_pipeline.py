import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sqlite3

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "9185033651:AAFiAhla50ZkEiQUz1FWyyaS_y0Ry9j9WSk"
TELEGRAM_CHAT_ID = "8887078816"

# Logging configuration setup
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logging.info("Telegram alert sent successfully.")
    except Exception as e:
        logging.error(f"Error sending Telegram alert: {str(e)}")

def extract_data():
    logging.info("1. EXTRACT: Multi-page Web scraping starting...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_books = []
    page = 1
    max_pages = 5
    
    try:
        while page <= max_pages:
            url = f'http://books.toscrape.com/catalogue/page-{page}.html'
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text
                availability = book.find('p', class_='instock availability').text.strip()
                
                all_books.append({
                    'Title': title,
                    'Price': price,
                    'Availability': availability
                })
            
            page += 1
            
        logging.info(f"Extraction successful: Total items fetched: {len(all_books)}")
        return pd.DataFrame(all_books)
        
    except Exception as e:
        error_msg = f"Extraction error: {str(e)}"
        logging.error(error_msg)
        return None

def transform_data(df):
    logging.info("2. TRANSFORM: Cleaning data...")
    try:
        df['Price'] = df['Price'].str.replace('Â', '', regex=False)
        df['Price'] = df['Price'].str.replace('£', '', regex=False)
        df['Price'] = pd.to_numeric(df['Price'])
        df['Availability'] = df['Availability'].str.strip()
        return df
    except Exception as e:
        logging.error(f"Transform error: {str(e)}")
        return None

def load_data(df):
    logging.info("3. LOAD: Saving to CSV & SQLite...")
    try:
        df.to_csv('automated_books_pipeline.csv', index=False)
        
        conn = sqlite3.connect('books.db')
        df.to_sql('books_info', conn, if_exists='replace', index=False)
        conn.close()
        
        success_msg = f"Multi-page ETL Success! Total items processed: {len(df)}"
        logging.info(success_msg)
        send_telegram_alert(f"✅ *ETL Pipeline Success!*\n\n{success_msg}")
        print("Pipeline execution complete! Multiple pages scraped and saved.")
    except Exception as e:
        logging.error(f"Load error: {str(e)}")

if __name__ == "__main__":
    logging.info("==== ETL Pipeline execution started ====")
    raw_df = extract_data()
    if raw_df is not None:
        cleaned_df = transform_data(raw_df)
        if cleaned_df is not None:
            load_data(cleaned_df)
    logging.info("==== ETL Pipeline execution ended ====\n")
