from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

# Routes for our page comes here #
@app.route('/')
def index():
	return render_template('index.html')


# Routes for sending Favicon #
@app.route('/favicon.ico')
def favicon():
	return send_from_directory("static/favicons", "favicon.ico")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)