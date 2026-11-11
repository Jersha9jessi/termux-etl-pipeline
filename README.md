# Termux Automated ETL Pipeline 🚀

A lightweight, automated ETL (Extract, Transform, Load) pipeline built entirely on **Termux (Android)**, scheduled using **Cron**, and integrated with **Telegram** for real-time alerts.

---

## 📌 Features
- **Extract:** Scrapes multi-page product data using Python (`requests` & `BeautifulSoup`).
- **Transform:** Cleans and formats raw HTML data.
- **Load:** Stores data in **SQLite Database (`books.db`)** and **CSV (`automated_books_pipeline.csv`)**.
- **Automation:** Fully automated using **Cronie** to run on a daily schedule.
- **Notifications:** Sends instant Telegram alerts upon execution.
- **Persistence:** Uses `termux-wake-lock` to keep tasks active in the background.

---

## 🛠️ Tech Stack
- **Language:** Python 3
- **Libraries:** `requests`, `BeautifulSoup`, `sqlite3`
- **Environment:** Termux (Android)
- **Scheduler:** Cron (`cronie`)
- **Alerts:** Telegram Bot API

