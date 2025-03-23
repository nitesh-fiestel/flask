# app/services/auth_service.py
from service.request import Request


class AuthService:
    @staticmethod
    def authenticate(username, password):
        user = Request.getUser(username)
        if user and user["password"] == password:
            return {"authenticated": True, "id": user["id"], "name": user["name"]}
        return {"authenticated": False}

