import json   # The json module is used to work with JSON data
import os     # The os module is used to interact with the operating system.


from flask import Flask, jsonify, request, send_file, send_from_directory


from langchain_core.messages import HumanMessage      # HumanMessage from langchain_core.messages: Represents a message from a human user.
from langchain_google_genai import ChatGoogleGenerativeAI   # ChatGoogleGenerativeAI from langchain_google_genai: Provides a chat interface for Google's generative AI.


# Creates a Flask web application named app.
app = Flask(__name__)

# Sets an environment variable GOOGLE_API_KEY with a specified API key.
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfrathnilONcu2o1If4dUzHNObPpWz760"; 

# Defines a route for the home page (/) that sends the index.html file from the web directory.
@app.route('/')
def home():
    return send_file('web/index.html')


# route for the /api/generate endpoint that accepts POST requests.
@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(
                content=content
            )
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


#  route to serve static files from the web directory for any given path.
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

# If the script is run directly, it starts the Flask app in debug mode.
if __name__ == '__main__':
    app.run(debug=True)