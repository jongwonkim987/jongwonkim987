from flask import Flask, render_template, request

app = Flask(__name__)

users = [
    {
        "username": "leo",
        "posts": [{"title": "Town House", "likes": 120}]
    },
    {
        "username": "alex",
        "posts": [{"title": "Mountain Climbing", "likes": 350}, {"title": "River Rafting", "likes": 200}]
    },
    {
        "username": "kim",
        "posts": [{"title": "Delicious Ramen", "likes": 230}]
    }
]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/users")
def get_users():
    return {"users": users}

@app.post("/users")
def create_user():
    request_data = request.get_json()
    new_user = {
        "username": request_data["username"],
        "posts": [{"title": "My First Post"}]
    }
    users.append(new_user)
    return new_user, 201

@app.post("/users/post/<string:username>")
def addd_post(username):
    request_data = request.get_json()
    for user in users:
        if user["username"] == username:
            new_post = {
                "title": request_data["title"],
                "likes": request_data["likes"]
            }
            user["posts"].append(new_post)
            return new_post, 201
    return {"error": "User not found"}, 404

@app.get("/users/post/<string:username>")
def get_user_posts(username):
    for user in users:
        if user["username"] == username:
            return {"posts": user["posts"]}, 200
    return {"error": "User not found"}, 404

@app.put("/users/post/like/<string:username>/<string:title>")
def like_post(username, title):
    for user in users:
        if user["username"] == username:
            for post in user["posts"]:
                if post["title"] == title:
                    post["likes"] += 1
                    return {"message": "Post liked"}, 200
            return {"error": "Post not found"}, 404
    return {"error": "User not found"}, 404

@app.delete("/users/<username>")
def delete_user(username):
    global users
    users = [user for user in users if user["username"] != username]
    return {"message": "User deleted"}, 200

if __name__ == "__main__":
    app.run(debug=True)