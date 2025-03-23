import requests

class Request:
    @staticmethod
    def get(url, user, password):
        response = requests.get('https://api.example.com/data')
        return response.json()
    @staticmethod
    def getAllUsers(url):
        response = requests.get(url)
        return response.json()["users"]
    @staticmethod
    def getUser(email):
        response = requests.get("http://localhost:8080/api/users?email=" + email)
        return response.json()


