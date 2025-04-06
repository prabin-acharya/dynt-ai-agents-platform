
from dotenv import load_dotenv
from flask import Flask

from routes.agents import bp as agents_bp
from routes.tools import bp as tools_bp
from routes.chat import bp as chat_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(agents_bp)
app.register_blueprint(tools_bp)
app.register_blueprint(chat_bp)


@app.route("/", methods=["GET"])
def hello():
    return {
        "message": "Welcome to Dynt — intelligent financial agent platform.",
        "status": "API is live and operational.",
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)

