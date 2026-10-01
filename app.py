import pandas as pd
import streamlit as st
from src.store import (
    all_rows,
    get_row,
    record_packet,
    row_to_listing,
    set_status,
    STATUSES,
)
from src.packet import generate
from src.tailor import TailorError

st.set_page_config(page_title="Job Tracker", layout="wide")
st.title("Job Application Tracker")

rows = all_rows()
if not rows:
    st.warning("No listings yet. Run the aggregator first.")
    st.stop()                                             # nothing to render, exit cleanly

df = pd.DataFrame(rows)
df["posted_date"] = df["posted_date"].str[:10]            # trim ISO timestamp to just the date
df["packet"] = df["packet_path"].notna().map({True: "✓", False: ""})   # draft generated?

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
    view[["company", "title", "location", "status", "packet", "posted_date", "url"]],
    width="stretch",
    hide_index=True,
    column_config={
        "packet": st.column_config.TextColumn("Draft", width="small"),
        "posted_date": st.column_config.TextColumn("Posted"),
        "url": st.column_config.LinkColumn("Link", display_text="Open"),
    },
)

# --- Select a listing ----------------------------------------------------
st.divider()
labels = {f"{r['company']} — {r['title']}": r["id"] for _, r in view.iterrows()}
if not labels:
    st.info("No listings match the current filters.")
    st.stop()

choice = st.selectbox("Selected listing", list(labels.keys()))
listing_id = labels[choice]
selected = df[df["id"] == listing_id].iloc[0]

left, right = st.columns(2)

# --- Status update -------------------------------------------------------
with left:
    st.subheader("Status")
    new_status = st.selectbox(
        "Set status", STATUSES, index=STATUSES.index(selected["status"])
    )
    if st.button("Save status"):
        set_status(listing_id, new_status)                # validated inside store.py
        st.success(f"Set to {new_status}")
        st.rerun()                                        # reload so the table reflects it

# --- Packet generation ---------------------------------------------------
with right:
    st.subheader("Review packet")
    st.caption("Generates a draft for you to review. Costs one API call. Submits nothing.")
    if st.button("Generate packet"):
        with st.spinner("Tailoring…"):                    # one call, never a loop
            try:
                listing = row_to_listing(get_row(listing_id))
                path = generate(listing)                   # writes only if tailoring succeeded
                record_packet(listing_id, str(path))       # tracker now reflects the draft
                st.session_state["last_packet"] = str(path)
                st.success(f"Written to {path}")
            except TailorError as exc:                     # API, parse, or missing-file failure
                st.error(f"Could not generate packet: {exc}")

    existing = selected["packet_path"]                     # may be NaN when the column has nulls
    if pd.isna(existing):                                  # NaN is truthy — check it explicitly
        existing = None
    current = st.session_state.get("last_packet") or existing
    if current:
        try:
            with open(current) as f:
                packet_text = f.read()
            st.download_button(                            # local file, no network
                "Download packet",
                packet_text,
                file_name=str(current).split("/")[-1],
                mime="text/markdown",
            )
            with st.expander("Preview packet"):
                st.markdown(packet_text)                   # our own generated text, safe to render
        except FileNotFoundError:                          # path recorded but file deleted
            st.warning("A packet was recorded for this listing but the file is missing.")

# --- Listing detail ------------------------------------------------------
with st.expander("Original listing text"):
    st.markdown(f"**{selected['title']}** at {selected['company']}")
    st.markdown(f"[View posting]({selected['url']})")
    st.text(selected["description"][:3000])                # st.text: untrusted content stays inert