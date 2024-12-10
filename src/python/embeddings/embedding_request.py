from flask import Flask

from flask_cors import CORS

app = Flask(__main__)


CORS(app)

@app.route("/api/embeddings", methods=["POST"])
def embeddings_request(req, res):
    return jsonify({
        })


if __name__ == "__main__":
    app.run(debug=False, port=8080)