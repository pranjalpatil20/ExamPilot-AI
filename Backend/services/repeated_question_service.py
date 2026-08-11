from database import get_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_repeated_questions():
    # Connect to database
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Read all questions
    sql = """
        SELECT id, question_text
        FROM questions
    """
    cursor.execute(sql)
    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    # If there are less than 2 questions, stop
    if len(questions) < 2:
        return 0

    # Store only question text
    question_texts = [question["question_text"] for question in questions]

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(question_texts)

    # Compare every question
    similarity_matrix = cosine_similarity(tfidf_matrix)

    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            similarity = similarity_matrix[i][j]
            if similarity >= 0.85:
                sql = """
                    INSERT INTO repeated_questions (question1_id, question2_id, similarity)
                    VALUES (%s, %s, %s)
                """
                values = (
                    questions[i]["id"],
                    questions[j]["id"],
                    float(similarity),
                )
                cursor.execute(sql, values)
                count += 1

    conn.commit()
    cursor.close()
    conn.close()

    return count
