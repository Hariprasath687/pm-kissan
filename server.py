from flask import Flask, render_template, send_from_directory, request, jsonify
import cx_Oracle
import json
app = Flask(__name__)

# Setting the json data from file
jsonfile = ""
with open("rawdata.json", "r", encoding="utf-8") as js:
	jsonfile = json.load(js)

# connection = cx_Oracle.connect("project","project")

# Routes for our page comes here #
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template("register.html")

# @app.route('/test')
# def test():
# 	cursor = connection.cursor()
# 	cursor.execute("CREATE TABLE testdb(firstname varchar(255),lastname varchar(255),phoneNumber number(12))")
# 	a = cursor.execute("DESCRIBE TestDB")
# 	print(a)
# 	return connection.version

@app.route('/liststates', methods=['POST'])
def getstates():
	listofstates = []
	for data in jsonfile["states"]:
		listofstates.append(
			{
				"state": data["name"],
				"districts": data["districts"]
			}
		)
	return jsonify({"result": listofstates})

# Routes for sending Favicon #
@app.route('/favicon.ico')
def favicon():
	return send_from_directory("static/favicons", "favicon.ico")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)