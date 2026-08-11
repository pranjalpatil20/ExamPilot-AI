# import mysql.connector
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="admin123",
#         database="exam_pilot_ai"
#     )
# print("Database module loaded successfully")

# import mysql.connector
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        use_pure=True
    )


print("Database module loaded successfully")

# import mysql.connector
# from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


# def get_connection():
#     return mysql.connector.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME,

#         ssl_ca="aiven-ca.pem",
#         ssl_verify_cert=True,

#         use_pure=True
#     )


# print("Database module loaded successfully")