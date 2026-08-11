# ==========================================================
# ExamPilot AI
# Explore Papers
# ==========================================================

import streamlit as st
import sys
import os
import requests


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

from utils.api_client import search_documents


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Explore Papers | ExamPilot AI",
    page_icon="📚",
    layout="wide"
)


# ==========================================================
# BACKEND URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ==========================================================
# SUBJECT DATA
# ==========================================================

BRANCH_SUBJECTS = {

    "Computer Engineering": {

        1: [
            "Basic Mathematics",
            "Communication Skill"
        ],

        2: [
            "Applied Mathematics",
            "Programming in C"
        ],

        3: [
            "Data Structure using C",
            "Database Management System",
            "Digital Techniques",
            "Object Oriented Programming using C++"
        ],

        4: [
            "Data Communication and Computer Network",
            "Java Programming",
            "Microproccessor Programming"
        ],

        5: [
            "Advance Computer Network",
            "Cloud Computing",
            "Data Analytics",
            "Operating System",
            "Software Engineering"
        ],

        6: [
            "Data Warehousing with Mining Techniques",
            "Digital Forensic and Hacking Techniques",
            "Machine Learning",
            "Software Testing"
        ]
    },


    "Artificial Intelligence & Machine Learning": {

        1: [
            "Basic Mathematics",
            "Communication Skill"
        ],

        2: [
            "Applied Mathematics",
            "Programming in C"
        ],

        3: [
            "Data Structure using Python",
            "Database Management System",
            "Digital Techniques",
            "Statistical Modelling using Machine Learning"
        ],

        4: [
            "Data Communication and Computer Network",
            "Java Programming",
            "Mathematics for ML",
            "Microproccessor Programming"
        ],

        5: [
            "Advance Database Management",
            "AI and ML Algorithms",
            "Cloud Computing for DS",
            "Natural Language Processing",
            "Operating System"
        ],

        6: [
            "Advanced Algorithm in AI and ML",
            "Big Data Analytics",
            "Data Warehousing with Mining Techniques",
            "Principles of Image Processing",
            "Reinforcement Learning"
        ]
    },


    "Computer Science and Information Technology": {

        1: [
            "Basic Mathematics",
            "Communication Skill"
        ],

        2: [
            "Applied Mathematics",
            "Programming in C"
        ],

        3: [
            "Data Structure using C",
            "Database Management System",
            "Digital Techniques and Microprocessores",
            "Object Oriented Programming using C++"
        ],

        4: [
            "Data Communication and Computer Network",
            "Information Security",
            "Java Programming"
        ],

        5: [
            "Advance Database Management",
            "Cloud Computing",
            "Data Analytics",
            "Operating System",
            "Software Engineering"
        ],

        6: [
            "Data Warehousing with Mining Techniques",
            "Digital Forensic and Hacking Techniques",
            "Machine Learning",
            "Software Testing"
        ]
    },


    "Electronics and Telecommunication": {

        1: [
            "Basic Mathematics",
            "Communication Skill"
        ],

        2: [
            "Applied Mathematics",
            "Basic Electronics",
            "Elements of Electrical Engineering"
        ],

        3: [
            "Analog Electronics",
            "Circuit and Networks",
            "Digital Techniques",
            "Principles of Electronic Communication"
        ],

        4: [
            "Basic Power Electronics",
            "Consumer Electronic Systems",
            "Digital Communication Systems",
            "Microcontroller and Applications"
        ],

        5: [
            "Advance Power Electronics",
            "Embedded System",
            "IOT Applications",
            "Microwave Engineering and Radar System",
            "Mobile and Wireless Communication"
        ],

        6: [
            "Automation and PLC",
            "Computer Network and Data Communication",
            "Drone Technology",
            "Optical Network and Satellite Communication",
            "VLSI Application"
        ]
    }
}


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F8FAFC;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #0F172A,
            #164E63
        );

        padding: 38px;
        border-radius: 22px;
        margin-bottom: 28px;
        color: white;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-text {
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
<div class="hero">
<div class="hero-title">
        Explore Previous Year Papers
</div>

<div class="hero-text">
        Find question papers by branch, semester, subject,
        examination year and exam type.
</div>
</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# FILTER SECTION
# ==========================================================

st.subheader("Find Your Paper")


# ==========================================================
# BRANCH
# ==========================================================

selected_branch = st.selectbox(
    "Branch",
    list(BRANCH_SUBJECTS.keys())
)


# ==========================================================
# SEMESTER
# ==========================================================

selected_semester = st.selectbox(
    "Semester",
    list(
        BRANCH_SUBJECTS[
            selected_branch
        ].keys()
    ),
    format_func=lambda x: f"Semester {x}"
)


# ==========================================================
# SUBJECT
# ==========================================================

selected_subject = st.selectbox(
    "Subject",
    BRANCH_SUBJECTS[
        selected_branch
    ][
        selected_semester
    ]
)


# ==========================================================
# YEAR + EXAM TYPE
# ==========================================================

col1, col2 = st.columns(2)


with col1:

    selected_year = st.selectbox(
        "Year",
        [2024, 2025, 2026]
    )


with col2:

    selected_exam_type = st.selectbox(
        "Exam Type",
        [
            "Summer",
            "Winter"
        ]
    )


st.write("")


# ==========================================================
# SEARCH BUTTON
# ==========================================================

search_clicked = st.button(
    "Search Papers",
    type="primary",
    use_container_width=True
)


# ==========================================================
# SEARCH RESULTS
# ==========================================================

if search_clicked:

    with st.spinner("Searching papers..."):

        result = search_documents(
            branch=selected_branch,
            semester=selected_semester,
            subject=selected_subject,
            year=selected_year,
            exam_type=selected_exam_type
        )

    # ======================================================
    # API ERROR
    # ======================================================

    if isinstance(result, dict) and result.get("error"):

        st.error(
            f"Search failed: {result['error']}"
        )

        st.session_state["search_results"] = []

    else:

        # Save results so they remain available
        # after Streamlit reruns

        st.session_state["search_results"] = result


# ==========================================================
# GET SAVED SEARCH RESULTS
# ==========================================================

result = st.session_state.get(
    "search_results",
    []
)


# ==========================================================
# DISPLAY SEARCH RESULTS
# ==========================================================

if result:

    st.divider()

    st.subheader(
        "Available Papers"
    )

    st.success(
        f"{len(result)} paper(s) found."
    )


    # ======================================================
    # DISPLAY PAPERS
    # ======================================================

    for index, document in enumerate(result):


        # ==================================================
        # DOCUMENT ID
        # ==================================================

        document_id = document.get("id")

        if document_id is None:

            document_id = document.get(
                "document_id"
            )


        # ==================================================
        # DOCUMENT INFORMATION
        # ==================================================

        title = document.get(
            "title",
            "Untitled Question Paper"
        )

        branch = document.get(
            "branch",
            selected_branch
        )

        semester = document.get(
            "semester",
            selected_semester
        )

        subject = document.get(
            "subject",
            selected_subject
        )

        year = document.get(
            "year",
            selected_year
        )

        exam_type = document.get(
            "exam_type",
            selected_exam_type
        )


        # ==================================================
        # PAPER CARD
        # ==================================================

        with st.container(border=True):

            st.markdown(
                f"### 📄 {title}"
            )

            st.write(
                f"**Branch:** {branch}"
            )

            st.write(
                f"**Semester:** {semester}"
            )

            st.write(
                f"**Subject:** {subject}"
            )

            st.write(
                f"**Year:** {year}"
            )

            st.write(
                f"**Exam Type:** {exam_type}"
            )

            st.write("")


            # ==================================================
            # BUTTONS
            # ==================================================

            button1, button2 = st.columns(2)


            # ==================================================
            # OPEN PDF
            # ==================================================

            with button1:

                if st.button(
                    "📄 Open PDF",
                    key=f"open_pdf_{document_id}_{index}",
                    use_container_width=True
                ):

                    if document_id is None:

                        st.error(
                            "Document ID is not available."
                        )

                    else:

                        st.session_state[
                            "selected_document_id"
                        ] = int(document_id)

                        st.session_state[
                            "selected_document"
                        ] = document

                        st.switch_page(
                            "pages/Open_PDF.py"
                        )


            # ==================================================
            # DOWNLOAD PDF
            # ==================================================

            with button2:

                if document_id is None:

                    st.warning(
                        "Document ID is not available."
                    )

                else:

                    try:

                        download_response = requests.get(
                            f"{BACKEND_URL}/documents/download/{document_id}",
                            timeout=30
                        )

                        if download_response.status_code == 200:

                            st.download_button(
                                label="⬇️ Download PDF",
                                data=download_response.content,
                                file_name=f"{title}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_{document_id}_{index}",
                                use_container_width=True
                            )

                        else:

                            st.error(
                                "PDF download failed."
                            )

                    except requests.exceptions.ConnectionError:

                        st.error(
                            "Cannot connect to Flask backend."
                        )

                    except requests.exceptions.Timeout:

                        st.error(
                            "Download request timed out."
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Download failed: {e}"
                        )


# ==========================================================
# NO RESULTS
# ==========================================================

elif search_clicked:

    st.warning(
        "No question paper found for the selected filters."
    )

    st.info(
        "Please try another year or exam type."
    )


# ==========================================================
# INFORMATION
# ==========================================================

st.divider()

st.subheader(
    "How to use"
)

st.write(
    "1. Select your Branch."
)

st.write(
    "2. Select the Semester."
)

st.write(
    "3. Select the required Subject."
)

st.write(
    "4. Select the Year."
)

st.write(
    "5. Select Summer or Winter."
)

st.write(
    "6. Click Search Papers."
)

st.write(
    "7. Click Open PDF to view the selected paper."
)

st.write(
    "8. Click Download PDF to download the selected paper."
)