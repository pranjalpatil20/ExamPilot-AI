import streamlit as st
import requests
import html


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Repeated Questions | ExamPilot AI",
    page_icon="",
    layout="wide"
)


# ==========================================================
# BACKEND
# ==========================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background: #F5F7FA;
}

.header {
    background: linear-gradient(135deg, #111827, #164E63);
    padding: 35px 40px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.header h1 {
    color: white;
    font-size: 34px;
    margin: 0;
}

.header p {
    color: #D1D5DB;
    margin-top: 10px;
    font-size: 15px;
}

.paper-box {
    background: white;
    padding: 18px 22px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    margin-bottom: 20px;
}

.stat-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #E2E8F0;
    text-align: center;
}

.stat-number {
    font-size: 30px;
    font-weight: 700;
    color: #0F766E;
}

.stat-label {
    font-size: 14px;
    color: #64748B;
    margin-top: 5px;
}

.question-card {
    background: white;
    padding: 22px;
    margin: 15px 0;
    border-radius: 14px;
    border-left: 5px solid #0F766E;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
}

.question-number {
    color: #0F766E;
    font-weight: 700;
    font-size: 15px;
    margin-bottom: 8px;
}

.question-text {
    color: #1E293B;
    font-size: 17px;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    margin-top: 12px;
    margin-right: 8px;
    padding: 6px 12px;
    border-radius: 20px;
    background: #ECFDF5;
    color: #047857;
    font-size: 12px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="header">
    <h1>Repeated Questions</h1>
    <p>
        View repeated questions detected for the selected
        previous year question paper.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# GET SELECTED PAPER ID
# ==========================================================

document_id = st.session_state.get("selected_document_id")


if not document_id:

    st.warning("Please select a question paper first.")

    if st.button("Go to Explore Papers"):

        st.switch_page("pages/Explore_pages.py")

    st.stop()


# ==========================================================
# SELECTED PAPER
# ==========================================================

st.markdown(
    f"""
<div class="paper-box">
        <b>Selected Paper ID:</b> {document_id}
</div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# API CALL
# ==========================================================

try:

    response = requests.get(
        f"{BACKEND_URL}/questions/repeated/{document_id}",
        timeout=30
    )

except requests.exceptions.ConnectionError:

    st.error(
        "Backend is not running. Start the Flask server first."
    )
    st.stop()

except requests.exceptions.Timeout:

    st.error(
        "Backend request timed out."
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
        f"Backend Error: {response.status_code}"
    )

    try:
        st.json(response.json())
    except:
        st.code(response.text)

    st.stop()


# ==========================================================
# JSON DATA
# ==========================================================

try:

    data = response.json()

except:

    st.error("Backend returned invalid JSON.")
    st.stop()


# ==========================================================
# HANDLE DIFFERENT RESPONSE FORMATS
# ==========================================================

if isinstance(data, dict):

    questions = (
        data.get("repeated_questions")
        or data.get("questions")
        or data.get("data")
        or []
    )

else:

    questions = data


# ==========================================================
# MAKE SURE QUESTIONS IS A LIST
# ==========================================================

if not isinstance(questions, list):

    questions = []


# ==========================================================
# STATISTICS
# ==========================================================

st.markdown(
    f"""
<div class="stat-card">
<div class="stat-number">{len(questions)}</div>
<div class="stat-label">Repeated Questions</div>
</div>
    """,
    unsafe_allow_html=True
)


st.write("")


# ==========================================================
# SEARCH
# ==========================================================

search = st.text_input(
    "Search repeated questions",
    placeholder="Type a keyword..."
)


# ==========================================================
# FILTER
# ==========================================================

if search.strip():

    search_value = search.lower().strip()

    filtered_questions = []

    for item in questions:

        if isinstance(item, dict):

            text = (
                item.get("question_text")
                or item.get("question")
                or item.get("text")
                or ""
            )

        else:

            text = str(item)

        if search_value in text.lower():

            filtered_questions.append(item)

else:

    filtered_questions = questions


# ==========================================================
# NO DATA
# ==========================================================

if not filtered_questions:

    st.info(
        "No repeated questions found for this paper."
    )

else:

    st.subheader(
        f"Repeated Questions ({len(filtered_questions)})"
    )


    # ======================================================
    # DISPLAY QUESTIONS
    # ======================================================

    for index, item in enumerate(
        filtered_questions,
        start=1
    ):

        if isinstance(item, dict):

            question_1 = item.get("question_1", "")
            question_2 = item.get("question_2", "")
            similarity = item.get("similarity", "")

            frequency = ""
            topic = ""

        else:

            question_1 = str(item)
            question_2 = ""
            similarity = ""

            frequency = ""
            topic = ""

        


            question_1 = html.escape(str(question_1))
            question_2 = html.escape(str(question_2))
            
            badges = ""

        if frequency:
            badges = (
                f'<span class="badge">'
                f'Repeated {html.escape(str(frequency))} times'
                f'</span>'
            )
            
        if topic:
            badges = (
            f'<span class="badge">'
            f'{html.escape(str(topic))}'
            f'</span>'
            )    

        if similarity:
            badges = (
            f'<span class="badge">'
            f'Similarity: {float(similarity) * 100:.1f}%'
            f'</span>'
            )


        st.markdown(
    f"""<div class="question-card">
<div class="question-number">
Question {index}
</div>

<div class="question-text">
<b>Question 1:</b><br>
{question_1}
<br><br>
<b>Question 2:</b><br>
{question_2}
</div>

{badges}

</div>""",
    unsafe_allow_html=True
)


# ==========================================================
# BACK BUTTON
# ==========================================================

st.write("")

if st.button(
    "Back to Explore Papers",
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

    