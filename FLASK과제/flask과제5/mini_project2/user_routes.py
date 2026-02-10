from flask import request
from user_model import add_user, add_post, get_user_posts, like_user_post, delete_user
from app import users

def register_user_routes(app):
    @app.route("/users", methods=["GET", "POST"])
    def users_route():
          if request.method == "GET":
              return {"users": users}
          elif request.method == "POST":
              request_data = request.get_json()
              return add_user(request_data)

    @app.route("/users/post/<string:username>", methods=["POST"])
    def create_post(username):
        request_data = request.get_json()
        return add_post(username, request_data)

    @app.route("/users/post/<string:username>", methods=["GET"])
    def fetch_user_posts(username):
        return get_user_posts(username)

    @app.route("/users/post/like/<string:username>/<string:title>", methods=["PUT"])
    def like_post(username, title):
        return like_user_post(username, title)

    @app.route("/users/<username>", methods=["DELETE"])
    def remove_user(username):
        return delete_user(username)
    
    return app