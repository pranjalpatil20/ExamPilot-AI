from flask import Flask, jsonify
from routes.auth_route import auth_bp
from routes.document_route import document_bp
from routes.pdf_route import pdf_bp
from routes.question_route import question_bp
from routes.repeated_question_route import repeated_question_bp
from routes.dashboard_route import dashboard_bp

# Create Flask App
app = Flask(__name__)

# Home Route
@app.route("/")
def hello_world():
     return "<p>ExamPilot-AI - Backend</p>"
    
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(document_bp, url_prefix="/documents")
app.register_blueprint(pdf_bp, url_prefix="/pdf")
app.register_blueprint(question_bp, url_prefix="/questions")
app.register_blueprint(repeated_question_bp,url_prefix="/repeated-questions")
app.register_blueprint(dashboard_bp)



# Run Flask Application
if __name__ == "__main__":
     print(app.url_map)
     app.run(debug=True,
          use_reloader=False
          )
     
     