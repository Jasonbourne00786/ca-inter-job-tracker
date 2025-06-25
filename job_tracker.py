
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="CA Inter Job Tracker", layout="wide")
st.title("📊 CA Inter MNC Job Tracker")

# User Inputs
job_title = st.text_input("Job Title", "CA Inter")
location = st.text_input("Location", "Ahmedabad or Remote")
search_button = st.button("Search Jobs")

# Job Fetching Function
def fetch_jobs_indeed(query, location):
    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": query,
        "l": location,
        "remotejob": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for card in soup.select(".job_seen_beacon"):
        title = card.find("h2").text.strip()
        company = card.find("span", class_="companyName").text.strip() if card.find("span", class_="companyName") else "N/A"
        location = card.find("div", class_="companyLocation").text.strip() if card.find("div", class_="companyLocation") else "N/A"
        link_tag = card.find("a")
        link = "https://www.indeed.com" + link_tag['href'] if link_tag else "#"

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link
        })
    return jobs

# Search Button Trigger
if search_button:
    with st.spinner("🔍 Searching for jobs..."):
        job_listings = fetch_jobs_indeed(job_title, location)

    if job_listings:
        for job in job_listings:
            st.markdown(f"### [{job['title']}]({job['link']})")
            st.write(f"**Company:** {job['company']}")
            st.write(f"**Location:** {job['location']}")
            st.markdown("---")
    else:
        st.warning("❌ No jobs found. Try changing the search query or location.")
