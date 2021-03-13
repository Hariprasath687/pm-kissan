from flask import Flask, render_template, send_from_directory
import cx_Oracle
app = Flask(__name__)

connection = cx_Oracle.connect("project","project")

# Routes for our page comes here #
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template("hehe.html")

@app.route('/test')
def test():
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE testdb(firstname varchar(255),lastname varchar(255),phoneNumber number(12))")
	a = cursor.execute("DESCRIBE TestDB")
	print(a)
	return connection.version

# Routes for sending Favicon #
@app.route('/favicon.ico')
def favicon():
	return send_from_directory("static/favicons", "favicon.ico")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)