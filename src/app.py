import pandas as pd
import streamlit as st
from src.store import all_rows, set_status, STATUSES

st.set_page_config(page_title="Job Tracker", layout="wide")
st.title("Job Application Tracker")

rows = all_rows()
if not rows:
    st.warning("No listings yet. Run the aggregator first.")
    st.stop()                                             # nothing to render, exit cleanly

df = pd.DataFrame(rows)
df["posted_date"] = df["posted_date"].str[:10]            # trim ISO timestamp to just the date

# --- Filters -------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.multiselect("Status", STATUSES, default=STATUSES)
with col2:
    company_filter = st.multiselect("Company", sorted(df["company"].unique()))
with col3:
    search = st.text_input("Search title")

view = df[df["status"].isin(status_filter)]               # pandas filtering, no SQL needed here
if company_filter:
    view = view[view["company"].isin(company_filter)]
if search:
    view = view[view["title"].str.contains(search, case=False, na=False)]

# --- Pipeline summary ----------------------------------------------------
counts = df["status"].value_counts()
cols = st.columns(len(STATUSES))
for col, status in zip(cols, STATUSES):
    col.metric(status, int(counts.get(status, 0)))        # .get: a status with 0 rows is missing

# --- Table ---------------------------------------------------------------
st.caption(f"Showing {len(view)} of {len(df)} listings")
st.dataframe(
    view[["company", "title", "location", "status", "posted_date", "url"]],
    width="stretch",                                      # replaces deprecated use_container_width
    hide_index=True,
    column_config={
        "posted_date": st.column_config.TextColumn("Posted"),
        "url": st.column_config.LinkColumn("Link", display_text="Open"),   # clickable posting link
    },
)

# --- Status update -------------------------------------------------------
st.subheader("Update status")
labels = {f"{r['company']} — {r['title']}": r["id"] for _, r in view.iterrows()}
if labels:
    choice = st.selectbox("Listing", list(labels.keys()))
    current = df[df["id"] == labels[choice]]["status"].iloc[0]
    new_status = st.selectbox("Status", STATUSES, index=STATUSES.index(current))
    if st.button("Save"):
        set_status(labels[choice], new_status)            # validated inside store.py
        st.success(f"Set to {new_status}")
        st.rerun()                                        # reload so the table reflects it

# --- Detail --------------------------------------------------------------
if labels:
    row = df[df["id"] == labels[choice]].iloc[0]
    with st.expander("Listing detail"):
        st.markdown(f"**{row['title']}** at {row['company']}")
        st.markdown(f"[View posting]({row['url']})")
        st.text(row["description"][:2000])                # st.text: untrusted content stays inert