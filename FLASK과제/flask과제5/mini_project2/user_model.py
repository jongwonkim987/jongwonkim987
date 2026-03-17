from app import users

def add_user(request_data):
    new_user = {
        "username": request_data["username"],
        "posts": []
    }
    users.append(new_user)
    return new_user, 201

def add_post(username, request_data):
    for user in users:
        if user["username"] == username:
            new_post = {
                "title": request_data["title"],
                "likes": 0
            }
            user["posts"].append(new_post)
            return new_post, 201
    return {"error": "User not found"}, 404

def get_user_posts(username):
    for user in users:
        if user["username"] == username:
            return {"posts": user["posts"]}, 200
    return {"error": "User not found"}, 404

def like_user_post(username, post_title):
    for user in users:
        if user["username"] == username:
            for post in user["posts"]:
                if post["title"] == post_title:
                    post["likes"] += 1
                    return {"message": "Post liked"}, 200
            return {"error": "Post not found"}, 404
    return {"error": "User not found"}, 404

def delete_user(username):
    global users
    users = [user for user in users if user["username"] != username]
    return {"message": "User deleted"}, 200