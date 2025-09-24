from datetime import datetime, timezone
import requests
import pandas as pd  

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1418734640729952256/Djt5Rk1RnhYdxNRMnfRHQY462lrRjvby2Cgl8cGu2UphtTKNvZ8CCMsPoSlTayFtuBTa"

def send_to_discord(job):
    message = f"""
📌 **{job['Role']}** at **{job['Company']}**
📍 {job['Location']}
🔗 [Apply Here]({job['Link']})
📣 Referral: {job['Referral Info']}
📝 {job['Notes']}
"""
    payload = {
        "content": message,
        "thread_name": f"{job['Role']} at {job['Company']}"[:90]  
    }
    response = requests.post(DISCORD_WEBHOOK, json=payload)

    if response.status_code == 204:
        print(f"Sent to Discord Forum: {job['Role']} at {job['Company']}")
    else:
        print(f"Failed | Status: {response.status_code} | {response.text}")


# --- HiringCafe Scraper ---
url = "https://hiring.cafe/api/search-jobs"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://hiring.cafe",
    "referer": "https://hiring.cafe/?searchState=%7B%22sortBy%22%3A%22date%22%2C%22searchQuery%22%3A%22Analyst%22%7D",
    "user-agent": "Mozilla/5.0"
}

payload = {
    "size": 100,
    "page": 0,
    "searchState": {
        "locations": [
            {
                "formatted_address": "United States",
                "types": ["country"],
                "id": "user_country",
                "address_components": [
                    {"long_name": "United States", "short_name": "US", "types": ["country"]}
                ],
                "options": {
                    "flexible_regions": ["anywhere_in_continent", "anywhere_in_world"]
                }
            }
        ],
        "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
        "commitmentTypes": [
            "Full Time", "Part Time", "Contract", "Internship",
            "Temporary", "Seasonal", "Volunteer"
        ],
        "roleTypes": ["Individual Contributor", "People Manager"],
        "seniorityLevel": [
            "No Prior Experience Required", "Entry Level", "Mid Level", "Senior Level"
        ],
        "searchQuery": "Analyst",
        "sortBy": "date"
    }
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
jobs = data.get("results", [])

# --- Filter jobs ≤ 24 hours ---
now = datetime.now(timezone.utc)
filtered_jobs = []

for job in jobs:
    job_data = job.get("v5_processed_job_data", {})
    posted_str = job_data.get("estimated_publish_date")

    if posted_str:
        posted_time = datetime.fromisoformat(posted_str.replace("Z", "+00:00"))
        hours_ago = (now - posted_time).total_seconds() / 3600

        if hours_ago <= 24:
            filtered_jobs.append({
                "Role": job_data.get("core_job_title", "N/A"),
                "Company": job_data.get("company_name", "N/A"),
                "Location": job_data.get("formatted_workplace_location", "N/A"),
                "Link": job.get("apply_url", "N/A"),
                "Referral Info": "-",
                "Notes": f"Responsibilities: {job_data.get('requirements_summary', 'N/A')} | Posted {round(hours_ago, 2)} hrs ago"
            })

# --- Pretty print + Send top 5 jobs ---
if filtered_jobs:
    top_jobs = filtered_jobs[:5] 
    df = pd.DataFrame(top_jobs)
    print(f"\n{len(top_jobs)} jobs found in the last 24 hours:\n")
    print(df.to_string(index=False))

    print("\nSending jobs to Discord Forum...\n")
    for job in top_jobs:
        send_to_discord(job)
else:
    print("No jobs posted in the last 24 hours.")
