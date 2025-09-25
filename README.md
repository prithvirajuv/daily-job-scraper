# 🧠 Daily Job Scraper

This project automatically finds the latest job postings and sends them to a Discord forum every day.

## 🔍 What it does

- Uses a **Python script** to search and collect the top 5 job postings shared in the last 24 hours.
- Gets details like:
  - Job title  
  - Company name  
  - Location  
  - Apply link  
  - Time it was posted
- Sends the job info straight to a **Discord forum** using a **webhook**.
- Runs **automatically every day at 12:30 PM (EST)** using **GitHub Actions** — no need to run it manually or save to Google Sheets.

## ⚙️ Tech used

- **Python**: To write the main job scraping and posting logic
- **REST API**: To fetch job listings
- **GitHub Actions**: To run the script daily
- **Discord Webhook**: To send the job details to a channel/forum

## 📅 How it works

1. GitHub Actions is set to run the script every day at 12:30 PM (Eastern Time).
2. The script pulls fresh job data from the API.
3. It formats the top 5 jobs nicely.
4. The message is sent directly to the chosen Discord forum.

---

