from flask import request, jsonify
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            jwt.decode(token, "your-jwt-secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator



# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         auth_header = request.headers.get("Authorization", None)

#         if not auth_header:
#             return jsonify({"message": "Authorization header is missing"}), 401

#         parts = auth_header.split()

#         if len(parts) != 2 or parts[0] != "Bearer":
#             return jsonify({"message": "Authorization header must be in the format: Bearer <token>"}), 401

#         token = parts[1]

#         try:
#             jwt.decode(token, "your-jwt-secret", algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 401

#         return f(*args, **kwargs)
#     return decorator