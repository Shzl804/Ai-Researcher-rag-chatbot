import os

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)


st.set_page_config(
    page_title="AI Researcher",
    page_icon="R",
    layout="wide",
)

st.title("AI Researcher")
st.write("Ask questions about your uploaded PDF documents.")


st.sidebar.header("Backend")

if st.sidebar.button("Check Backend"):
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=10,
        )

        if response.ok:
            st.sidebar.success("Backend is running")
        else:
            st.sidebar.error("Backend returned an error")

    except requests.RequestException:
        st.sidebar.error("Could not connect to FastAPI")


st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
)

if st.sidebar.button("Process PDF"):
    if uploaded_file is None:
        st.sidebar.warning("Please choose a PDF first.")
    else:
        try:
            with st.spinner("Processing PDF..."):
                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    },
                    timeout=300,
                )

            if response.ok:
                result = response.json()

                st.sidebar.success("PDF processed successfully")

                st.session_state["document_info"] = result

            else:
                st.sidebar.error(
                    f"Upload failed: {response.text}"
                )

        except requests.RequestException as error:
            st.sidebar.error(
                f"Connection error: {error}"
            )


if "document_info" in st.session_state:
    document_info = st.session_state["document_info"]

    st.info(
        f"Document: {document_info['source']} | "
        f"Pages: {document_info['pages']} | "
        f"Chunks: {document_info['chunks']}"
    )


st.header("Ask a Question")

question = st.text_area(
    "Enter your question",
    placeholder="What is machine learning?",
)

number_of_results = st.slider(
    "Number of retrieved chunks",
    min_value=1,
    max_value=8,
    value=4,
)


if st.button("Ask Question", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching documents and generating answer..."):
                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": question,
                        "number_of_results": number_of_results,
                    },
                    timeout=300,
                )

            if response.ok:
                result = response.json()

                st.subheader("Answer")
                st.write(result.get("answer", "No answer returned."))

                st.subheader("Sources")

                sources = result.get("sources", [])

                if sources:
                    for index, source in enumerate(
                        sources,
                        start=1,
                    ):
                        st.write(
                            f"[{index}] "
                            f"{source['source']} - "
                            f"Page {source['page']}"
                        )
                else:
                    st.write("No sources were returned.")

            else:
                st.error(
                    f"Query failed: {response.text}"
                )

        except requests.RequestException as error:
            st.error(
                f"Connection error: {error}"
            )