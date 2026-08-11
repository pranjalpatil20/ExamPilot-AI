from flask import Blueprint
from controllers.auth_controller import signup, login

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(signup)
auth_bp.route("/login", methods=["POST"])(login)
