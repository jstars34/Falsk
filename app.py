from flask import Flask,jsonify
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
import  random
quotes = [
    'hamza',
    'bukari'
    'abdirashid',
    'qass',
]
@app.route('/get_quote', methods=['GET'])
def get_quote():
    return jsonify({"quote":random.choice(quotes)})
if __name__ == "__main__":
    app.run(debug=True)
