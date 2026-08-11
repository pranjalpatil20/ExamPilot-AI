# ==========================================================
# ExamPilot AI
# Dashboard
# ==========================================================

import streamlit as st
import requests
import sys
import os


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
    page_title="Dashboard | ExamPilot AI",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# BACKEND URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ==========================================================
# CSS
# ==========================================================

st.markdown(
"""
<style>

.dashboard-hero {
    background: linear-gradient(135deg, #0F172A, #164E63);
    padding: 38px;
    border-radius: 22px;
    margin-bottom: 28px;
    color: white;
}

.dashboard-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.dashboard-subtitle {
    font-size: 16px;
    color: #CBD5E1;
}

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #0F172A;
    margin-top: 10px;
    margin-bottom: 18px;
}

.stat-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    min-height: 150px;
}

.stat-title {
    font-size: 15px;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 34px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 6px;
}

.stat-description {
    font-size: 13px;
    color: #94A3B8;
}

.info-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
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
<div class="dashboard-hero">
<div class="dashboard-title">
ExamPilot AI Dashboard
</div>

<div class="dashboard-subtitle">
Overview of question papers, extracted questions
and repeated-question analysis.
</div>
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# GET DASHBOARD DATA
# ==========================================================

def get_dashboard_stats():

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard/stats",
            timeout=30
        )

        if response.status_code != 200:

            return {
                "error": (
                    f"Backend returned status "
                    f"{response.status_code}"
                )
            }

        return response.json()

    except requests.exceptions.ConnectionError:

        return {
            "error": (
                "Unable to connect to Flask backend. "
                "Make sure the backend is running."
            )
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Dashboard request timed out."
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": str(e)
        }

    except ValueError:

        return {
            "error": "Backend returned invalid JSON."
        }


# ==========================================================
# LOAD DATA
# ==========================================================

if "dashboard_stats" not in st.session_state:

    st.session_state["dashboard_stats"] = (
        get_dashboard_stats()
    )


stats = st.session_state["dashboard_stats"]


# ==========================================================
# REFRESH BUTTON
# ==========================================================

refresh_col1, refresh_col2 = st.columns(
    [5, 1]
)

with refresh_col2:

    if st.button(
        "Refresh Data",
        use_container_width=True
    ):

        st.session_state["dashboard_stats"] = (
            get_dashboard_stats()
        )

        st.rerun()


# ==========================================================
# API ERROR
# ==========================================================

if isinstance(stats, dict) and stats.get("error"):

    st.error(
        stats["error"]
    )

    st.stop()


# ==========================================================
# READ STATISTICS
# ==========================================================

total_pdfs = stats.get(
    "total_pdfs",
    0
)

total_questions = stats.get(
    "total_questions",
    0
)

repeated_questions = stats.get(
    "repeated_questions",
    0
)

supported_branches = stats.get(
    "supported_branches",
    4
)


# ==========================================================
# PROJECT OVERVIEW
# ==========================================================

st.markdown(
"""
<div class="section-title">
Project Overview
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# STAT CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(
    4
)


# ----------------------------------------------------------
# TOTAL PAPERS
# ----------------------------------------------------------

with col1:

    st.markdown(
"""
<div class="stat-card">
<div class="stat-title">
Total Question Papers
</div>

<div class="stat-value">
%s
</div>

<div class="stat-description">
Uploaded PDF documents
</div>
</div>
""" % total_pdfs,
    unsafe_allow_html=True
    )


# ----------------------------------------------------------
# TOTAL QUESTIONS
# ----------------------------------------------------------

with col2:

    st.markdown(
"""
<div class="stat-card">
<div class="stat-title">
Total Questions
</div>

<div class="stat-value">
%s
</div>

<div class="stat-description">
Extracted from papers
</div>
</div>
""" % total_questions,
    unsafe_allow_html=True
    )


# ----------------------------------------------------------
# REPEATED QUESTIONS
# ----------------------------------------------------------

with col3:

    st.markdown(
"""
<div class="stat-card">
<div class="stat-title">
Repeated Questions
</div>

<div class="stat-value">
%s
</div>

<div class="stat-description">
Detected question repetitions
</div>
</div>
""" % repeated_questions,
    unsafe_allow_html=True
    )


# ----------------------------------------------------------
# SUPPORTED BRANCHES
# ----------------------------------------------------------

with col4:

    st.markdown(
"""
<div class="stat-card">
<div class="stat-title">
Supported Branches
</div>

<div class="stat-value">
%s
</div>

<div class="stat-description">
Available academic branches
</div>
</div>
""" % supported_branches,
    unsafe_allow_html=True
    )


# ==========================================================
# SPACE
# ==========================================================

st.write("")
st.write("")


# ==========================================================
# QUESTION ANALYTICS
# ==========================================================

st.markdown(
"""
<div class="section-title">
Question Analytics
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# ANALYTICS COLUMNS
# ==========================================================

chart_col1, chart_col2 = st.columns(
    2
)


# ==========================================================
# QUESTION DISTRIBUTION
# ==========================================================

with chart_col1:

    st.markdown(
"""
<div class="info-card">
<div class="stat-title">
Question Distribution
</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.metric(
        "Total Questions",
        total_questions
    )


# ==========================================================
# REPEATED QUESTION ANALYSIS
# ==========================================================

with chart_col2:

    st.markdown(
"""
<div class="info-card">
<div class="stat-title">
Repeated Question Analysis
</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.metric(
        "Repeated Questions",
        repeated_questions
    )


# ==========================================================
# QUESTIONS BY BRANCH
# ==========================================================

st.write("")
st.markdown(
"""
<div class="section-title">
Questions by Branch
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# BRANCH DATA
# ==========================================================

branch_data = stats.get(
    "questions_by_branch",
    {}
)


if branch_data:

    st.bar_chart(
        branch_data
    )

else:

    st.info(
        "Branch-wise question data is not available yet."
    )


# ==========================================================
# QUESTIONS BY SEMESTER
# ==========================================================

st.write("")

st.markdown(
"""
<div class="section-title">
Questions by Semester
</div>
""",
unsafe_allow_html=True
)


# ==========================================================
# SEMESTER DATA
# ==========================================================

semester_data = stats.get(
    "questions_by_semester",
    {}
)


if semester_data:

    st.bar_chart(
        semester_data
    )

else:

    st.info(
        "Semester-wise question data is not available yet."
    )


# ==========================================================
# PROJECT SUMMARY
# ==========================================================

st.write("")
st.divider()

st.markdown(
"""
<div class="section-title">
ExamPilot AI
</div>
""",
unsafe_allow_html=True
)

st.write(
    "ExamPilot AI analyzes previous year question papers, "
    "extracts questions and identifies repeated questions "
    "to help students prepare more effectively."
)
