from flask import Flask, url_for, render_template, request, jsonify
import Analyzer

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/analyze/')
def analyze():
	username = request.args.get('key', '')
	if username != '':
		res = Analyzer.analyze(username)
		res['success'] = True
	else:
		res = {'success': False}
	return jsonify(res)

if __name__ == '__main__':
	app.run(debug = True)