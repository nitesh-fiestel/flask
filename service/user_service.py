import requests, json

class UserService:

    @staticmethod
    def getFollowers(userId):
        resp = requests.get("http://localhost:8080/api/users/followers?userId=" + str(userId))

    @staticmethod
    def getFollowing(userId):
        return requests.get("http://localhost:8080/api/users/following?userId=" + str(userId)).json()

    @staticmethod
    def getFeed(userId, users):
        resp = requests.get("http://localhost:8080/api/users/" + str(userId) + "/feed").json()
        feed = []
        name = "NA"
        for row in resp:
            for email in users:
                if users[email]["id"] == row["userId"]:
                    name = users[email]["name"]
            feed.append({
                "content": row["content"],
                "username": name
            })
        return feed

    @staticmethod
    def follow(userId, followingId):
        url = "http://localhost:8080/api/users/follow"

        payload = json.dumps({
            "followerId": userId,
            "followingId": followingId
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

    @staticmethod
    def unfollow(userId, unFollowingId):
        url = "http://localhost:8080/api/users/unfollow"

        payload = json.dumps({
            "followerId": userId,
            "followingId": unFollowingId
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)