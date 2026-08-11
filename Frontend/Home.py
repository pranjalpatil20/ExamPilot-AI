# ==========================================================
# ExamPilot AI
# Professional Streamlit Home Page
# Premium UI Version
# ==========================================================

import streamlit as st


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ExamPilot AI",
    page_icon="📚",
    layout="wide"
)



# ---------------- CUSTOM CSS ----------------

st.markdown("""
            


<style>

/* Button Styling */

.stButton > button {

    background-color:#2563EB;

    color:white;

    border-radius:10px;

    border:none;

    padding:8px 20px;

    font-weight:600;

}


.stButton > button:hover {

    background-color:#10B981;

    color:white;

}


.main {

    background:#F8FAFC;

}



/* Navbar */

.nav-box {

    background:white;

    padding:15px 25px;

    border-radius:15px;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.08);

}



/* Hero */

.hero {

    background:linear-gradient(
        135deg,
        #0F172A,
        #2563EB
    );

    padding:70px 50px;

    border-radius:25px;

    color:white;

}



.hero-title {

    font-size:48px;

    font-weight:800;

}



.hero-text {

    font-size:20px;

    color:#E2E8F0;

    margin-top:20px;

}




/* Cards */


.card {

    background:white;

    padding:25px;

    border-radius:18px;

    text-align:center;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.08);

}



.card h1 {

    color:#2563EB;

    font-size:40px;

}




/* Feature */


.feature-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    border-left: 6px solid #10B981;
    box-shadow: 0px 8px 25px rgba(15, 23, 42, 0.08);
    min-height: 220px;
    height: auto;
    box-sizing: border-box;
}



.feature-card h3 {

    color:#0F172A;

}




/* Workflow */


.workflow {

    background:#EFF6FF;

    padding:30px;

    border-radius:20px;

    text-align:center;

    border:1px solid #BFDBFE;

}




/* Technology */


.tech-card {

    background:white;

    padding:20px;

    text-align:center;

    border-radius:15px;

    box-shadow:
    0px 4px 15px rgba(0,0,0,0.06);

}




/* Footer */


.footer {

    text-align:center;

    color:#64748B;

    padding:30px;

}


</style>

""",
unsafe_allow_html=True)




# ---------------- NAVBAR ----------------


n1,n2,n3 = st.columns([4,1,1])


with n1:

    st.markdown(
    """
    <h2 style="
    color:#2563EB;
    ">
    📚 ExamPilot AI
    </h2>
    """,
    unsafe_allow_html=True
    )


with n2:

    st.button(
        "Explore"
    )


with n3:

    st.button(
        "Login"
    )



st.write("")



# ---------------- HERO SECTION ----------------


st.markdown(
"""

<div class="hero">


<div class="hero-title">

AI Powered
<br>
Previous Year Question Paper Analyzer

</div>


<div class="hero-text">

Analyze previous year papers,
discover repeated questions,
find important topics and
prepare smarter using AI.

</div>


</div>

""",
unsafe_allow_html=True
)



st.write("")



st.button(
    "🚀 Explore Papers",
    type="primary"
)


st.divider()



# ---------------- STATISTICS ----------------


st.subheader(
    "Platform Statistics"
)



s1,s2,s3,s4 = st.columns(4)



stats = [

("260+","Question Papers"),

("1600+","Extracted Questions"),

("700+","Important Topics"),

("85%","Analysis Accuracy")

]



for col,data in zip(
    [s1,s2,s3,s4],
    stats
):

    with col:

        st.markdown(
        f"""

        <div class="card">

        <h1>
        {data[0]}
        </h1>

        <p>
        {data[1]}
        </p>

        </div>

        """,
        unsafe_allow_html=True
        )



st.divider()



# ---------------- FEATURES ----------------


st.subheader(
    "AI Features"
)



f1,f2,f3 = st.columns(3)



features=[


(
"📄 Smart PDF Extraction",
"Extract questions automatically from uploaded papers."
),


(
"🔁 Repeated Question Detection",
"Find frequently asked questions and patterns."
),


(
"🧠 AI Insights",
"Analyze topics, marks and difficulty level."
)


]



for col,item in zip(
    [f1,f2,f3],
    features
):

    with col:

        st.markdown(

        f"""

        <div class="feature-card">


        <h3>
        {item[0]}
        </h3>


        <p>
        {item[1]}
        </p>


        </div>

        """,

        unsafe_allow_html=True

        )



st.write("")



# ---------------- WORKFLOW ----------------


st.subheader(
    "How It Works"
)



w1,w2,w3 = st.columns(3)



workflow=[


(
"1️⃣ Upload PDF",
"Upload previous year question papers."
),


(
"2️⃣ AI Processing",
"Extract and analyze questions."
),


(
"3️⃣ Get Insights",
"View repeated questions and trends."
)

]



for col,item in zip(
    [w1,w2,w3],
    workflow
):

    with col:

        st.markdown(

        f"""

        <div class="workflow">


        <h3>
        {item[0]}
        </h3>


        <p>
        {item[1]}
        </p>


        </div>

        """,

        unsafe_allow_html=True

        )



st.divider()



# ---------------- TECHNOLOGY STACK ----------------


st.subheader(
    "Technology Stack"
)



t1,t2,t3,t4,t5 = st.columns(5)



technology=[

("🐍","Python"),

("🎨","Streamlit"),

("🔥","Flask"),

("🗄️","MySQL"),

("🤖","NLP")

]



for col,item in zip(
    [t1,t2,t3,t4,t5],
    technology
):

    with col:

        st.markdown(

        f"""

        <div class="tech-card">

        <h2>
        {item[0]}
        </h2>

        <p>
        {item[1]}
        </p>

        </div>

        """,

        unsafe_allow_html=True

        )



st.divider()



# ---------------- FOOTER ----------------


st.markdown(

"""

<div class="footer">


<b>ExamPilot AI</b>

<br>

AI Powered PYQ Analysis Platform


</div>

""",

unsafe_allow_html=True

)
