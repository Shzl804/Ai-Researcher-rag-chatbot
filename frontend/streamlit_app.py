import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Researcher",
    page_icon="🔎",
    layout="wide",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; max-width: 1000px; }
    .app-title { font-size: 2.2rem; font-weight: 700; margin-bottom: 0; }
    .app-subtitle { color: #8a8a8a; font-size: 1rem; margin-top: 0.2rem; margin-bottom: 1.5rem; }
    .source-badge {
        display: inline-block;
        background-color: #eef2ff;
        color: #3730a3;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        margin: 3px 4px 3px 0;
    }
    .status-dot {
        height: 10px; width: 10px; border-radius: 50%;
        display: inline-block; margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_status" not in st.session_state:
    st.session_state.backend_status = None


def check_backend():
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        st.session_state.backend_status = "online" if response.ok else "error"
    except requests.RequestException:
        st.session_state.backend_status = "offline"


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Backend status")

    if st.session_state.backend_status is None:
        check_backend()

    status = st.session_state.backend_status
    color = {"online": "#22c55e", "offline": "#ef4444", "error": "#f59e0b"}.get(status, "#9ca3af")
    label = {"online": "Connected", "offline": "Not reachable", "error": "Responding with errors"}.get(status, "Unknown")
    st.markdown(
        f'<span class="status-dot" style="background-color:{color};"></span>{label}',
        unsafe_allow_html=True,
    )
    if st.button("Recheck"):
        check_backend()
        st.rerun()

    st.divider()

    st.header("Settings")
    number_of_results = st.slider("Chunks to retrieve", min_value=1, max_value=8, value=4)

    st.divider()

    st.header("Add a document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file and st.button("Index document", type="primary", use_container_width=True):
        with st.spinner("Indexing document..."):
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                    timeout=300,
                )
                if response.ok:
                    info = response.json()
                    st.success(f"Indexed {info.get('source')} — {info.get('chunks')} chunks")
                else:
                    st.error(f"Upload failed: {response.text}")
            except requests.RequestException as error:
                st.error(f"Connection error: {error}")

# ---------- Main area ----------
st.markdown('<p class="app-title">AI Researcher</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Ask questions about your indexed documents — answers are grounded and cited.</p>',
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("sources"):
            badges = "".join(
                f'<span class="source-badge">{s["source"]} · p.{s["page"]}</span>'
                for s in message["sources"]
            )
            st.markdown(badges, unsafe_allow_html=True)

question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": question, "number_of_results": number_of_results},
                    timeout=300,
                )
                if response.ok:
                    result = response.json()
                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])

                    st.write(answer)
                    if sources:
                        badges = "".join(
                            f'<span class="source-badge">{s["source"]} · p.{s["page"]}</span>'
                            for s in sources
                        )
                        st.markdown(badges, unsafe_allow_html=True)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "sources": sources}
                    )
                else:
                    error_text = f"Query failed: {response.text}"
                    st.error(error_text)
                    st.session_state.messages.append({"role": "assistant", "content": error_text})
            except requests.RequestException as error:
                error_text = f"Connection error: {error}"
                st.error(error_text)
                st.session_state.messages.append({"role": "assistant", "content": error_text})