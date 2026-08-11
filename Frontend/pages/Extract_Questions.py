# ==========================================================
# ExamPilot AI
# Extract Questions
# ==========================================================

import streamlit as st
import requests
import sys
import os
import html


# ==========================================================
# PROJECT PATH
# ==========================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Extract Questions | ExamPilot AI",
    page_icon="📄",
    layout="wide"
)


# ==========================================================
# BACKEND URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

.hero {
    background: linear-gradient(135deg, #0F172A, #164E63);
    padding: 38px;
    border-radius: 22px;
    margin-bottom: 28px;
    color: white;
}

.page-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.page-subtitle {
    font-size: 16px;
    color: #CBD5E1;
}

.summary-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.summary-number {
    font-size: 30px;
    font-weight: 800;
    color: #0F766E;
}

.summary-label {
    font-size: 14px;
    color: #64748B;
    margin-top: 6px;
}

.question-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #0F766E;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.question-number {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 8px;
}

.sub-question {
    display: inline-block;
    background: #CCFBF1;
    color: #115E59;
    padding: 5px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
}

.marks {
    display: inline-block;
    background: #F1F5F9;
    color: #475569;
    padding: 5px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
    margin-left: 6px;
}

.question-text {
    font-size: 16px;
    line-height: 1.6;
    color: #334155;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    """<div class="hero"><div class="page-title">Extract Questions</div><div class="page-subtitle">View questions extracted from the selected question paper.</div></div>""",
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
# NO PAPER SELECTED
# ==========================================================

if document_id is None:

    st.warning(
        "No question paper selected."
    )

    st.info(
        "Please go to Explore Papers and select a question paper first."
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

st.markdown(
    f"""<div style="background:white;padding:12px 18px;border-radius:12px;border:1px solid #E2E8F0;margin-bottom:20px;"><b>Selected Paper ID:</b> {document_id}</div>""",
    unsafe_allow_html=True
)


# ==========================================================
# DOCUMENT DETAILS
# ==========================================================

if document:

    title = html.escape(
        str(document.get("title", "Question Paper"))
    )

    subject = html.escape(
        str(document.get("subject", "-"))
    )

    year = html.escape(
        str(document.get("year", "-"))
    )

    exam_type = html.escape(
        str(document.get("exam_type", "-"))
    )

    st.markdown(
        f"""<div style="background:white;padding:18px 22px;border-radius:16px;border:1px solid #E2E8F0;margin-bottom:25px;"><b>Paper:</b> {title}<br><b>Subject:</b> {subject}<br><b>Year:</b> {year}<br><b>Exam Type:</b> {exam_type}</div>""",
        unsafe_allow_html=True
    )


# ==========================================================
# LOAD QUESTIONS
# ==========================================================

with st.spinner(
    "Loading extracted questions..."
):

    try:

        response = requests.get(
            f"{BACKEND_URL}/questions/{document_id}",
            timeout=30
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to the Flask backend."
        )

        st.info(
            "Make sure the Flask backend is running on port 5000."
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error(
            "Backend request timed out."
        )

        st.stop()

    except requests.exceptions.RequestException as e:

        st.error(
            f"Request error: {e}"
        )

        st.stop()


# ==========================================================
# API RESPONSE
# ==========================================================

if response.status_code != 200:

    st.error(
        f"Backend returned status code: {response.status_code}"
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
# PARSE JSON
# ==========================================================

try:

    data = response.json()

except ValueError:

    st.error(
        "Backend returned an invalid JSON response."
    )

    st.text(
        response.text
    )

    st.stop()


# ==========================================================
# GET QUESTIONS
# ==========================================================

if isinstance(data, dict):

    questions = data.get(
        "questions",
        []
    )

else:

    questions = data


# ==========================================================
# NO QUESTIONS
# ==========================================================

if not questions:

    st.warning(
        "No extracted questions found for this paper."
    )

    st.info(
        "Questions may not have been extracted for this document yet."
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
# QUESTION STATISTICS
# ==========================================================

total_questions = len(questions)

main_question_numbers = set()

sub_question_count = 0

total_marks = 0


for question in questions:

    if not isinstance(question, dict):
        continue

    question_no = question.get(
        "question_no"
    )

    if question_no is not None:

        main_question_numbers.add(
            str(question_no)
        )

    if question.get("sub_question"):

        sub_question_count += 1

    marks = question.get(
        "marks"
    )

    if marks is not None:

        try:

            total_marks += int(marks)

        except (ValueError, TypeError):

            pass


main_questions = len(
    main_question_numbers
)


# ==========================================================
# SUMMARY
# ==========================================================

st.markdown(
    "## Extraction Summary"
)


summary1, summary2, summary3 = st.columns(3)


with summary1:

    st.markdown(
        f"""<div class="summary-card"><div class="summary-number">{main_questions}</div><div class="summary-label">Main Questions</div></div>""",
        unsafe_allow_html=True
    )


with summary2:

    st.markdown(
        f"""<div class="summary-card"><div class="summary-number">{sub_question_count}</div><div class="summary-label">Sub-Questions</div></div>""",
        unsafe_allow_html=True
    )


with summary3:

    st.markdown(
        f"""<div class="summary-card"><div class="summary-number">{total_marks}</div><div class="summary-label">Total Marks</div></div>""",
        unsafe_allow_html=True
    )


# ==========================================================
# QUESTIONS HEADER
# ==========================================================

st.write("")

st.markdown(
    "## Extracted Questions"
)

st.success(
    f"{total_questions} question(s) extracted successfully."
)


# ==========================================================
# DISPLAY QUESTIONS
# ==========================================================

for index, question in enumerate(
    questions,
    start=1
):

    # ------------------------------------------------------
    # CHECK QUESTION TYPE
    # ------------------------------------------------------

    if not isinstance(question, dict):

        question_text = str(
            question
        )

        question_no = str(
            index
        )

        sub_question = ""

        marks = ""

    else:

        question_text = question.get(
            "question_text",
            ""
        )

        question_no = question.get(
            "question_no",
            index
        )

        sub_question = question.get(
            "sub_question",
            ""
        )

        marks = question.get(
            "marks",
            ""
        )


    # ------------------------------------------------------
    # ESCAPE HTML
    # ------------------------------------------------------

    question_text = html.escape(
        str(question_text)
    )

    question_no = html.escape(
        str(question_no)
    )

    sub_question = html.escape(
        str(sub_question)
    )

    marks = html.escape(
        str(marks)
    )


    # ------------------------------------------------------
    # SUB QUESTION LABEL
    # ------------------------------------------------------

    sub_html = ""

    if sub_question:

        sub_html = (
            f'<span class="sub-question">'
            f'Sub-question {sub_question}'
            f'</span>'
        )


    # ------------------------------------------------------
    # MARKS LABEL
    # ------------------------------------------------------

    marks_html = ""

    if marks:

        marks_html = (
            f'<span class="marks">'
            f'{marks} Marks'
            f'</span>'
        )


    # ------------------------------------------------------
    # QUESTION CARD
    # ------------------------------------------------------

    st.markdown(
        f"""<div class="question-card"><div class="question-number">Question {question_no}</div>{sub_html}{marks_html}<div class="question-text">{question_text}</div></div>""",
        unsafe_allow_html=True
    )


# ==========================================================
# BACK BUTTON
# ==========================================================

st.write("")

st.divider()

if st.button(
    "← Back to Explore Papers",
    use_container_width=True
):

    st.switch_page(
        "pages/Explore_pages.py"
    )



st.info(
    "Note: If you see unusual symbols such as □, , , or similar "
    "PDF encoding characters, ignore those symbols and check the original "
    "paper/PDF for the correct mathematical symbol or notation."
)

