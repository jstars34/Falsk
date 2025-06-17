from flask import Flask,jsonify,request
from flask_cors import CORS 
import re
import time
API_KEY = '123456'
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
import  random
bad_keywords = ['utws', 'utwsmzg', '}{nijtx', '}s}}', 'wjiyzgj', '~tzutws', '}}}', '6=0', 'fizqy%{nijt', 'xj}%{nijt', 
                'kwjj%utws', '|fyhm%utws', 'utws%xnyj', 'jwtynh%{nijt', 'szij', 'sziny~', 'szijlnwqx', 'xj}%yfuj', 'mjsyfn',
                'fsfq', 'gqt|otg', 'lfslgfsl', 'rfxyzwgfynts', 'rnqk', 'nshjxy', 'qjxgnfs', 'lf~%utws', 'frfyjzw%utws', 'mtrjrfij%utws',
                'mfwihtwj', 'hwjfrunj', 'mjsyfn%utws', 'gnl%gttgx', 'xj}%xhjsj', 'utwsxyfw', 'ymwjjxtrj', 'szij%|trjs', '|jghfr%lnwqx', 'hfr%lnwqx',
                'inwy~%{nijt', 'xtqt%lnwq', '|mfy%nx%}s}}', 'mt|%yt%|fyhm%fizqy%{nijtx', 'fizqy%rt{nj', 'mty%lnwq%{nijt', 'xj}~%{nijtx', 
                '|fyhm%mty%lnwqx', 'mt|%yt%mf{j%xj}', '|fyhm%lnwqx', 'lnwqx%pnxxnsl', 'xj}~%|trfs', 'qt{j%{nijt', 'pnxx%xhjsjx',
                '6=%uqzx%rt{nj', 'lnwqx%|nymtzy%hqtymjx', 'zshjsxtwji%{nijt', 'xunh~%{nijt', 'wtrfsynh%{nijt%ltsj%|wtsl',
                '|mjwj%yt%knsi%}}}', 'sfzlmy~%hqnu', 'xjhwjy%xnyj%yt%|fyhm%}}}', 'mt|%yt%knsi%utws',
                'ytu%fizqy%{nijtx', 'kfrtzx%fizqy%fhywjxxjx', 'mt|%yt%pnqq%r~xjqk', 'xznhnij%rjymtix',
                'mt|%yt%gz~%iwzlx', 'hthfnsj', 'rfwnozfsf', 'gz~%|jji%tsqnsj', 'nqqjlfq%xnyjx', 'ifwp%|jg',
                'gqfhp%rfwpjy', 'xhmttq%xmttynsl', 'mt|%yt%rfpj%f%gtrg', 'xjqk2mfwr', 'mt|%yt%hzy%{jnsx', 't{jwitxj',
                'ifsljwtzx%ifwjx', 'xj}ynsl', 'mttp%zu%fuu', 'hmfy%|nym%xywfsljwx', 'rjjy%mty%xnslqjx', 'ynsijw%szijx',
                'kqnwy%hmfy', 'knsi%lnwqkwnjsi%tsqnsj', 'xsfuhmfy%lnwqx', 'xj}y', 'xjsi%szijx', 'tsq~kfsx']
def q(t):
    a = list(t);y = ''
    for l in a:y += chr(ord(l) - 5)
    return y
bad_keywords = [q(a) for a in bad_keywords]
def clean_text(t):
    text = t.lower()
    text = re.sub(r'[^a-z0-9\s]','',text)
    return text
def is_inappropriate(text):
    cleaned = clean_text(text)
    for keyword in bad_keywords: 
        if keyword in cleaned:
            return True
    return False


@app.route('/submit_name', methods=['GET'])
def submit_name():
    name = request.args.get('name')
    if name:
        bad_keywords.append(name)
        return jsonify({"message": f"Hello, {name}!", "all_names": bad_keywords})
    return jsonify({"error": "No name provided"}), 400


@app.route('/message', methods=['POST'])
def message_api():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f'Bearer {API_KEY}':
        return jsonify({'error':"Unauthorized"}),401
    data = request.get_json()
    message = data.get('message','')
    response  = is_inappropriate(message)
    time.sleep(2)
    return jsonify({"response":f"{response}"})


# API Endpoint to add new bad keyword
@app.route('/add-bad-word', methods=['POST'])
def add_bad_word():
    try:
        data = request.json
        if not data or 'word' not in data:
            return jsonify({"error": "Bad Request. 'word' is required"}), 400

        new_word = clean_text(data['word'])

        if new_word in bad_keywords:
            return jsonify({"message": f"'{new_word}' already exists."}), 200

        bad_keywords.add(new_word)
        return jsonify({"message": f"'{new_word}' added to bad keywords."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error Handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "400 - Bad Request"}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "401 - Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "403 - Forbidden"}), 403

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "404 - Not Found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "500 - Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
