from functools import wraps
import jwt
import os
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from pymongo import MongoClient


SECRET_KEY = os.getenv("JWT_SECRET_KEY") 



auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

#  user database
client = MongoClient("mongodb+srv://agarwalkashish207:ayyeBainganchoubisa007@cluster0.kp3b99f.mongodb.net/")
db = client["Resume_Screener_AI"]
users_collection = db["users"]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # JWT is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Expecting: "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if users_collection.find_one({"email" : email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    users_collection.insert_one({
        "email": email,
        "password" : hashed_password
    })

    

    # users[email] = hashed_password
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({"email": email})


    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid user details"}), 401

    token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
    return jsonify({"token": token}), 200