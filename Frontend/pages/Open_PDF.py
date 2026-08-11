# ==========================================================
# ExamPilot AI
# Open PDF
# ==========================================================

import streamlit as st
import requests
import base64


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Open PDF | ExamPilot AI",
    page_icon="📄",
    layout="wide"
)


# ==========================================================
# BACKEND URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ==========================================================
# HERO CSS
# ==========================================================

st.markdown(
    """
    <style>

    .pdf-hero {
        background: linear-gradient(
            135deg,
            #0F172A,
            #164E63
        );

        padding: 35px;
        border-radius: 22px;
        margin-bottom: 25px;
        color: white;
    }

    .pdf-title {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .pdf-subtitle {
        font-size: 16px;
        color: #CBD5E1;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    """
<div class="pdf-hero">

<div class="pdf-title">
            Open Question Paper
</div>

<div class="pdf-subtitle">
            View the selected previous year question paper.
</div>

</div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# GET SELECTED DOCUMENT
# ==========================================================

document_id = st.session_state.get(
    "selected_document_id"
)

document = st.session_state.get(
    "selected_document",
    {}
)


# ==========================================================
# NO DOCUMENT
# ==========================================================

if document_id is None:

    st.warning(
        "No question paper selected."
    )

    if st.button(
        "← Back to Explore Papers",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Explore_pages.py"
        )

    st.stop()


# ==========================================================
# DOCUMENT INFORMATION
# ==========================================================

st.caption(
    f"Selected Paper ID: {document_id}"
)

if document:

    st.write(
        f"**Paper:** {document.get('title', 'Question Paper')}"
    )

    st.write(
        f"**Subject:** {document.get('subject', '-')}"
    )

    st.write(
        f"**Year:** {document.get('year', '-')}"
    )

    st.write(
        f"**Exam Type:** {document.get('exam_type', '-')}"
    )


# ==========================================================
# LOAD PDF
# ==========================================================

with st.spinner(
    "Loading question paper..."
):

    try:

        response = requests.get(
    f"{BACKEND_URL}/documents/open/{document_id}",
    timeout=30
)
    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to Flask backend."
        )

        st.info(
            "Make sure Flask is running on port 5000."
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error(
            "PDF request timed out."
        )

        st.stop()

    except requests.exceptions.RequestException as e:

        st.error(
            f"Request failed: {e}"
        )

        st.stop()


# ==========================================================
# RESPONSE CHECK
# ==========================================================

if response.status_code != 200:

    st.error(
        f"Unable to open PDF. "
        f"Backend returned {response.status_code}."
    )

    try:

        st.json(
            response.json()
        )

    except Exception:

        st.text(
            response.text
        )

    st.stop()


# ==========================================================
# PDF BYTES
# ==========================================================

pdf_bytes = response.content


if not pdf_bytes:

    st.error(
        "Backend returned an empty PDF."
    )

    st.stop()


# ==========================================================
# PDF PREVIEW
# ==========================================================

pdf_base64 = base64.b64encode(
    pdf_bytes
).decode("utf-8")


pdf_display = f"""
<iframe
    src="data:application/pdf;base64,{pdf_base64}"
    width="100%"
    height="850"
    style="
        border: 1px solid #CBD5E1;
        border-radius: 12px;
    ">
</iframe>
"""


st.markdown(
    pdf_display,
    unsafe_allow_html=True
)


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

st.write("")

st.download_button(
    label="Download PDF",
    data=pdf_bytes,
    file_name=f"question_paper_{document_id}.pdf",
    mime="application/pdf",
    use_container_width=True
)


# ==========================================================
# NAVIGATION
# ==========================================================

st.write("")

col1, col2 = st.columns(2)


# ==========================================================
# BACK
# ==========================================================

with col1:

    if st.button(
        "← Back to Explore Papers",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Explore_pages.py"
        )


# ==========================================================
# EXTRACT QUESTIONS
# ==========================================================

with col2:

    if st.button(
        "Extract Questions →",
        use_container_width=True
    ):

        st.session_state[
            "selected_document_id"
        ] = int(document_id)

        st.switch_page(
            "pages/Extract_Questions.py"
        )


# ==========================================================
# REPEATED QUESTIONS
# ==========================================================

if st.button(
    "Repeated Questions",
    use_container_width=True
):

    st.session_state[
        "selected_document_id"
    ] = int(document_id)

    st.switch_page(
        "pages/Repeated_Questions.py"
    )