from flask import Flask
from flask_smorest import Api
from api import blp as api_blp

app = Flask(__name__)

app.config["API_TITLE"] = "Book API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"

api = Api(app)
api.register_blueprint(api_blp)


if __name__ == '__main__':
    app.run(debug=True)
