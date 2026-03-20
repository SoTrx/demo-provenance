import asyncio

import streamlit as st
from kiota_abstractions.api_error import APIError

from api import compute_provenance_async, poll_for_provenance, serialize
from generated.ap_explanation.models.task_status_response import TaskStatusResponse
from llm import client
from utils import extract_formula_expressions, extract_sql_query, load_pg_json_from_file

TITLE = "Provenance Demo"
QUESTIONS = {
    "Select a question…": None,
    "Topics where students got level-4 questions from lecturer 78 wrong ": "assets/explain_sql_query_mathe.json",
}

st.set_page_config(page_title=TITLE, layout="centered")

st.title(TITLE)
st.markdown("Pick a question to compute its provenance")

selected = st.selectbox("Choose a question", list(QUESTIONS.keys()))

if not QUESTIONS.get(selected):
    st.info("Select a question from the dropdown to see results here.")
    st.stop()


# ── Resolve AP ──────────────────────────────
with st.spinner("Fetching…"):
    try:
        body = load_pg_json_from_file(QUESTIONS[selected])
        query = extract_sql_query(body)
        task_id = asyncio.run(compute_provenance_async(body))
        st.subheader("SQL Query")
        st.code(query, language="sql")
        provenance = asyncio.run(poll_for_provenance(task_id))
    except APIError as exc:
        st.error(f"Request failed with status {exc.response_status_code}")
        st.stop()

if provenance.status != "success":
    st.error(f"Task ended with status **{provenance.status}**")
    if provenance.error:
        st.json(serialize(provenance.error))
    st.stop()

formula_expressions = extract_formula_expressions(provenance)

st.subheader("Provenance expressions")
for i, expr in enumerate(formula_expressions, 1):
    st.markdown(f"**Result {i}:** `{expr}`")

st.divider()


if st.button("▶ Interpret Provenance", type="secondary", use_container_width=True):
    with st.spinner("Making sense of provenance…"):
        result = client.explain(
            "openai/kimi-k2.5",
            query,
            provenance,
        )

    st.subheader("Explanation")
    st.write(result)
