
import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.title("📋 Job Shop Scheduler")

st.sidebar.header("Submit New Job")
job_id = st.sidebar.text_input("Job ID")
duration = st.sidebar.number_input("Duration", min_value=1, step=1)
due_date = st.sidebar.number_input("Due Date", min_value=1, step=1)
machine = st.sidebar.text_input("Machine")
skill = st.sidebar.text_input("Skill")

if st.sidebar.button("Add Job"):
    payload = {
        "job_id": job_id,
        "duration": duration,
        "due_date": due_date,
        "machine_required": machine,
        "skill_required": skill
    }
    try:
        r = requests.post(f"{API_BASE}/jobs", json=payload)
        if r.status_code == 200:
            st.sidebar.success("✅ Job submitted.")
        else:
            st.sidebar.error(f"❌ Failed: {r.text}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"❌ API Error: {e}")

st.subheader("📊 Current Jobs")
try:
    jobs = requests.get(f"{API_BASE}/jobs").json()
    st.dataframe(pd.DataFrame(jobs))
except:
    st.warning("Could not fetch job data. Is the API running?")

st.subheader("📅 Current Schedule")
try:
    sched = requests.get(f"{API_BASE}/schedule").json()
    st.dataframe(pd.DataFrame(sched))
except:
    st.warning("Could not fetch schedule data. Is the API running?")
