from flask import Flask
from flask import render_template, redirect
from flask import Response, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('setup-landing.html')


if __name__ == "__main__":
	app.run(debug=True)
