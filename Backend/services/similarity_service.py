from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_repeated_questions(questions, threshold=0.75):

    texts = []

    for q in questions:
        text = q["question_text"]

        if text:
            texts.append(text.lower())


    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(texts)


    similarity_matrix = cosine_similarity(vectors)


    repeated = []


    for i in range(len(texts)):

        for j in range(i + 1, len(texts)):

            score = similarity_matrix[i][j]


            if score >= threshold:

                repeated.append({

                    "question_1": texts[i],

                    "question_2": texts[j],

                    "similarity": round(float(score),2)

                })


    return repeated