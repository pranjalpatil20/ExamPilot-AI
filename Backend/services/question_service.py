# ==========================================================
# ExamPilot AI
# Question Service
# ==========================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import get_connection
import re


# ==========================================================
# CLEAN QUESTION TEXT
# ==========================================================

def clean_question_text(text):

    if not text:
        return ""

    # Remove common PDF noise
    text = re.sub(
        r"\bP\.T\.O\.\b",
        " ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bSeat\s*No\.?\b",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Remove page/header noise such as:
    # 316319
    # 3 Hours / 70 Marks
    text = re.sub(
        r"\b\d{6}\b",
        " ",
        text
    )

    text = re.sub(
        r"\b\d+\s*Hours\s*/\s*\d+\s*Marks\b",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Remove patterns such as:
    # [ 2 ] Marks
    # [ 3 ] Marks
    text = re.sub(
        r"\[\s*\d+\s*\]\s*Marks",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ==========================================================
# GET QUESTIONS BY DOCUMENT
# ==========================================================

def get_questions_by_document(document_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        id,
        document_id,
        question_no,
        sub_question,
        marks,
        question_text,
        created_at
    FROM questions
    WHERE document_id = %s
    ORDER BY
        CAST(question_no AS UNSIGNED),
        sub_question
    """

    cursor.execute(
        query,
        (document_id,)
    )

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return questions


# ==========================================================
# EXTRACT TOP LEVEL QUESTIONS
# ==========================================================

def extract_top_level_questions(text):

    # Normalize PDF text
    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    # ------------------------------------------------------
    # Match:
    #
    # 1.
    # 1)
    # 2.
    # 2)
    #
    # while keeping the complete block
    # ------------------------------------------------------

    pattern = re.compile(
        r"(?m)^\s*(\d{1,2})\s*[\.\)]\s+(.*?)(?=^\s*\d{1,2}\s*[\.\)]\s+|\Z)",
        re.DOTALL
    )

    matches = pattern.findall(text)

    return matches


# ==========================================================
# DETERMINE MARKS
# ==========================================================

def determine_marks(question_block):

    # ------------------------------------------------------
    # Example:
    #
    # Attempt any FIVE ... : 10
    #
    # 10 / 5 = 2 marks
    #
    # Attempt any THREE ... : 12
    #
    # 12 / 3 = 4 marks
    #
    # Attempt any TWO ... : 12
    #
    # 12 / 2 = 6 marks
    # ------------------------------------------------------

    match = re.search(
        r"Attempt\s+any\s+"
        r"(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)"
        r".*?"
        r"(\d{1,2})",
        question_block,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    number_word = match.group(1).upper()
    total_marks = int(match.group(2))

    number_map = {
        "ONE": 1,
        "TWO": 2,
        "THREE": 3,
        "FOUR": 4,
        "FIVE": 5,
        "SIX": 6,
        "SEVEN": 7,
        "EIGHT": 8,
        "NINE": 9,
        "TEN": 10
    }

    required_questions = number_map.get(
        number_word
    )

    if not required_questions:
        return None

    if total_marks % required_questions != 0:
        return None

    marks = total_marks // required_questions

    # We only want 2, 4 and 6 marks
    if marks not in (2, 4, 6):
        return None

    return marks


# ==========================================================
# EXTRACT SUB QUESTIONS
# ==========================================================

def extract_sub_questions(question_block):

    # ------------------------------------------------------
    # Find:
    #
    # a)
    # b)
    # c)
    #
    # The pattern stops when another a), b), c)... starts.
    # ------------------------------------------------------

    pattern = re.compile(
        r"(?<!\w)([a-g])\s*[\)\.]\s+"
        r"(.*?)(?=(?<!\w)[a-g]\s*[\)\.]\s+|\Z)",
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(
        question_block
    )

    return matches


# ==========================================================
# EXTRACT QUESTIONS FROM TEXT
# ==========================================================

def extract_questions_from_text(text):

    questions = []

    if not text:
        return questions

    top_level_questions = extract_top_level_questions(
        text
    )

    for question_no, question_block in top_level_questions:

        question_block = question_block.strip()

        # Determine marks for this section
        marks = determine_marks(
            question_block
        )

        # Find subquestions
        sub_questions = extract_sub_questions(
            question_block
        )

        # --------------------------------------------------
        # If subquestions were found
        # --------------------------------------------------

        if sub_questions:

            for sub_question, sub_question_text in sub_questions:

                cleaned_text = clean_question_text(
                    sub_question_text
                )

                if len(cleaned_text) < 5:
                    continue

                questions.append({

                    "question_no": str(
                        question_no
                    ),

                    "sub_question": sub_question.lower(),

                    "marks": marks,

                    "question_text": cleaned_text
                })

        # --------------------------------------------------
        # Fallback:
        # If no a), b), c) structure was detected
        # --------------------------------------------------

        else:

            cleaned_text = clean_question_text(
                question_block
            )

            if len(cleaned_text) < 10:
                continue

            questions.append({

                "question_no": str(
                    question_no
                ),

                "sub_question": None,

                "marks": marks,

                "question_text": cleaned_text
            })

    return questions


# ==========================================================
# SAVE QUESTIONS
# ==========================================================

def save_questions(document_id, questions):

    if not questions:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # Remove old questions for this document
    # ------------------------------------------------------

    delete_query = """
    DELETE FROM questions
    WHERE document_id = %s
    """

    cursor.execute(
        delete_query,
        (document_id,)
    )

    # ------------------------------------------------------
    # Insert new questions
    # ------------------------------------------------------

    insert_query = """
    INSERT INTO questions
    (
        document_id,
        question_no,
        sub_question,
        marks,
        question_text
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    values = []

    for question in questions:

        values.append(
            (
                document_id,
                question["question_no"],
                question["sub_question"],
                question["marks"],
                question["question_text"]
            )
        )

    cursor.executemany(
        insert_query,
        values
    )

    conn.commit()

    inserted_count = cursor.rowcount

    cursor.close()
    conn.close()

    return inserted_count


# ==========================================================
# EXTRACT AND SAVE QUESTIONS FOR DOCUMENT
# ==========================================================

def extract_and_save_questions(document_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT extracted_text
    FROM extracted_text
    WHERE document_id = %s
    ORDER BY id DESC
    LIMIT 1
    """

    cursor.execute(
        query,
        (document_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:

        return {
            "success": False,
            "message": "No extracted text found.",
            "total_questions": 0
        }

    text = result["extracted_text"]

    questions = extract_questions_from_text(
        text
    )

    inserted = save_questions(
        document_id,
        questions
    )

    return {

        "success": True,

        "document_id": document_id,

        "total_questions": inserted,

        "questions": questions
    }


# ==========================================================
# REPEATED QUESTIONS
# ==========================================================

def get_repeated_questions(document_id):

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ------------------------------------------------------
    # Get questions from selected document
    # ONLY 2, 4 and 6 marks
    # ------------------------------------------------------

    query = """
    SELECT
        q.id,
        q.document_id,
        q.question_no,
        q.sub_question,
        q.marks,
        q.question_text,
        d.year,
        d.exam_type,
        d.subject
    FROM questions q
    JOIN documents d
        ON q.document_id = d.id
    WHERE q.document_id = %s
      AND q.marks IN (2, 4, 6)
    ORDER BY q.id
    """

    cursor.execute(
        query,
        (document_id,)
    )

    selected_questions = cursor.fetchall()

    # ------------------------------------------------------
    # Get questions from other documents
    #
    # Same marks category is compared with same marks
    # ------------------------------------------------------

    query = """
    SELECT
        q.id,
        q.document_id,
        q.question_no,
        q.sub_question,
        q.marks,
        q.question_text,
        d.year,
        d.exam_type,
        d.subject
    FROM questions q
    JOIN documents d
        ON q.document_id = d.id
    WHERE q.document_id != %s
      AND q.marks IN (2, 4, 6)
    ORDER BY q.id
    """

    cursor.execute(
        query,
        (document_id,)
    )

    other_questions = cursor.fetchall()

    cursor.close()
    conn.close()

    if not selected_questions or not other_questions:
        return []

    repeated = []

    # ------------------------------------------------------
    # Process each marks category separately
    # ------------------------------------------------------

    for marks in (2, 4, 6):

        selected_by_marks = [
            q for q in selected_questions
            if q["marks"] == marks
        ]

        other_by_marks = [
            q for q in other_questions
            if q["marks"] == marks
        ]

        if not selected_by_marks or not other_by_marks:
            continue

        selected_texts = [
            q["question_text"]
            for q in selected_by_marks
        ]

        other_texts = [
            q["question_text"]
            for q in other_by_marks
        ]

        all_texts = (
            selected_texts +
            other_texts
        )

        try:

            vectorizer = TfidfVectorizer(
                stop_words="english"
            )

            matrix = vectorizer.fit_transform(
                all_texts
            )

            similarity_matrix = cosine_similarity(
                matrix
            )

        except ValueError:
            continue

        selected_count = len(
            selected_by_marks
        )

        # --------------------------------------------------
        # Compare selected questions
        # against other papers
        # --------------------------------------------------

        for i in range(selected_count):

            best_match = None
            best_similarity = 0

            for j in range(
                selected_count,
                len(all_texts)
            ):

                similarity = similarity_matrix[i][j]

                if (
                    similarity >= 0.70
                    and similarity > best_similarity
                ):

                    best_similarity = similarity

                    best_match = other_by_marks[
                        j - selected_count
                    ]

            if best_match:

                repeated.append({

                    "question_id":
                        selected_by_marks[i]["id"],

                    "question_no":
                        selected_by_marks[i]["question_no"],

                    "sub_question":
                        selected_by_marks[i]["sub_question"],

                    "marks":
                        marks,

                    "question_text":
                        selected_by_marks[i]["question_text"],

                    "repeat_question":
                        best_match["question_text"],

                    "repeat_document_id":
                        best_match["document_id"],

                    "repeat_year":
                        best_match["year"],

                    "repeat_exam_type":
                        best_match["exam_type"],

                    "similarity":
                        round(
                            best_similarity,
                            2
                        )
                })

    return repeated


# ==========================================================
# GET ALL QUESTIONS
# ==========================================================

def get_all_questions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        id,
        document_id,
        question_no,
        sub_question,
        marks,
        question_text
    FROM questions
    """

    cursor.execute(query)

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return questions


# ==========================================================
# SEARCH QUESTIONS
# ==========================================================

def search_questions(keyword):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        q.id,
        q.question_text,
        q.document_id,
        q.question_no,
        q.sub_question,
        q.marks,
        d.subject,
        d.year,
        d.exam_type
    FROM questions q
    JOIN documents d
        ON q.document_id = d.id
    WHERE q.question_text LIKE %s
    """

    cursor.execute(
        query,
        ("%" + keyword + "%",)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def find_repeated_questions(questions, threshold=0.40):

    if not questions or len(questions) < 2:
        return []

    # ------------------------------------------------------
    # Convert questions into TF-IDF vectors
    # ------------------------------------------------------
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(questions)

    # ------------------------------------------------------
    # Calculate cosine similarity
    # ------------------------------------------------------
    similarity_matrix = cosine_similarity(tfidf_matrix)

    repeated_questions = []

    # ------------------------------------------------------
    # Compare every question with every other question
    # ------------------------------------------------------
    for i in range(len(questions)):

        for j in range(i + 1, len(questions)):

            similarity = similarity_matrix[i][j]

            if similarity >= threshold:

                repeated_questions.append({
                    "question_1": questions[i],
                    "question_2": questions[j],
                    "similarity": round(float(similarity), 2)
                })

    # Highest similarity first
    repeated_questions.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return repeated_questions