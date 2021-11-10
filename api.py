from flask import Flask, jsonify, request

app= Flask(__name__)

@app.route("/search", methods=["GET"])
def getSearchResults():
    query = request.headers.get('query')
    # Call ranking method to retrieve search results
    return jsonify("Retrieved")

if __name__=='__main__':
    app.run(debug=True)