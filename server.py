from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from flask.globals import session
from flask.helpers import url_for
import requests
import AESCipher
import cx_Oracle
import fingerprint
import json
from argon2 import PasswordHasher

app = Flask(__name__)
ph = PasswordHasher()
app.secret_key = "RGAGDGYU@719319788*@&@&@,,.s"
connection = cx_Oracle.connect("project","project")
secret_pwd = "Hanover Karens Allover place"

# Setting the json data from file
jsonfile = ""
with open("rawdata.json", "r", encoding="utf-8") as js:
	jsonfile = json.load(js)

# Routes for our page comes here #
@app.route('/')
def index():
	try:
		if session["username"]:
			return render_template('dashboard.html', username=session["username"])
	except:
		return render_template('index.html')

@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/login')
def login():
	try:
		if session["username"]:
			return redirect(url_for(".index"), 307)
	except:
		return render_template("login.html")

@app.route('/logi', methods=['POST'])
def loginuser():
	username = request.json["username"]
	UserPwd = request.json["pass"]
	_db_usr = "padips"
	_db_pwd_hashed = "$argon2id$v=19$m=102400,t=2,p=8$eIKCIMl8XhkjCtjo2RKx2Q$+oYxlVHIV6mdDid+5k7x3g"
	# 1) find the user from db.
	# 2) if exist then get their password
	passWordHasher = PasswordHasher()
	if username == _db_usr:
		if passWordHasher.verify(_db_pwd_hashed, UserPwd):
			session["username"] = _db_usr
			return jsonify({"result": "true"})
		else:
			return render_template("login.html", err="Username or password does not match!")

@app.route('/fingerpintverify', methods=["POST"])
def verifyFingerprint():
	print("getting req")
	myFP = fingerprint.FingerPrint()
	try:
		myFP.open()
		print("Please touch the fingerprint sensor")
		if myFP.verify():
			print("Hello! Master")
			print("Verified")
			return jsonify({"authorizedUser": "true"})
		else:
			print("Sorry! Man")
			return jsonify({"authorizedUser": "false"})
	except:
		print("Exception")
		return jsonify({"authorizedUser": "false"})
	finally:
		myFP.close()		

@app.route('/verifyAadhaar', methods=['POST'])
def aadhaar_verify():
	le_aadhar_number = (request.json["aadhaar"]).replace(" ","")
	cursor = connection.cursor()
	cx = cursor.execute("SELECT * from aadhaar_demo")
	for enc_data in cx:
		aadhaar_enc = enc_data[0]
		mobile_enc = enc_data[5]
		print(enc_data[0])
		
		dictVal = json.loads(enc_data[0])
		dec_val = AESCipher.decrypt(dictVal, password=secret_pwd)
		print("Decrypted val : " + str(dec_val))
		print("Encoded val " + str(le_aadhar_number))
		if le_aadhar_number == dec_val.decode("utf-8"):
			return jsonify({"Result": "verfied"})
		else:
			return jsonify({"Result": "Not valid"})

# Get the data and put them on the DB
@app.route('/sucessVerified', methods=['POST'])
def verifiedUser():
	userData = request.json
	firstName = userData["firstname"]
	lastName = userData["lastname"]
	fatherName = userData["fatherfirstname"] + " " + userData["fatherlastname"]
	dob =  userData["dob"]
	gender = userData["gender"]
	category = userData["category"]
	district = userData["district"]
	subdistrict = userData["subdistrict"]
	block = userData["block"]
	state = userData["state"]
	village = userData["village"]
	pincode = userData["pincode"]
	aadhaar = userData["aadhaar"]
	smartcard = userData["smartcard"]
	phoneno = userData["phoneno"]
	bankIFSC = userData["bankIFSC"]
	bankName = userData["bankName"]
	bankAccNumber = userData["bankAccNumber"]
	bankAccName = userData["bankAccName"]
	landstate = userData["landstate"]
	landDist = userData["landDist"]
	landtypearea = userData["landtypearea"]
	taluk = userData["taluk"]
	landvillage = userData["landvillage"]
	pattaNumber = userData["pattaNumber"]
	surveyNumber = userData["surveyNumber"]
	subDivisonNumber = userData["subDivisonNumber"]
	ownerName = userData["ownerName"]
	wardNumber = userData["wardNumber"]
	blockNumber = userData["blockNumber"]
	dataland = userData["dataland"]
	stringified_dataland = json.dumps(dataland)
	print(
		firstName,
		lastName,
		fatherName,
		dob,
		gender,
		category,
		district,
		subdistrict,
		block,
		state,
		village,
		pincode,
		aadhaar,
		smartcard,
		phoneno,
		bankIFSC,
		bankName,
		bankAccNumber,
		bankAccName,
		landstate,
		landDist,
		landtypearea,
		taluk,
		landvillage,
		pattaNumber,
		surveyNumber,
		subDivisonNumber,
		ownerName,
		wardNumber,
		blockNumber,
		stringified_dataland
		)
	return jsonify({"result": "ok"})

@app.route('/pending.Application')
def pendingApplication():
	pass

@app.route('/approvedApp')
def approvedApp():
	pass

@app.route('/yetReview')
def yetReview():
	pass

@app.route('/DeclinedApp')
def DeclinedApp():
	pass

@app.route('/logout')
def logout():
	try:
		session.pop("username", None)
		return redirect(url_for(".index"), 307)
	except:
		return redirect(url_for(".index"), 307)

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

@app.route('/getbankdata', methods=['POST'])
def getbankdata():
	ifsccode = request.json
	req = requests.get("https://ifsc.razorpay.com/"+ifsccode["ifsc"])
	req.encoding = "utf-8"	
	return jsonify({"res": req.json()})

# Routes for sending Favicon #
@app.route('/favicon.ico')
def favicon():
	return send_from_directory("static/favicons", "favicon.ico")


# @app.route('/test')
# def test():
# 	cursor = connection.cursor()
# 	cursor.execute("CREATE TABLE testdb(firstname varchar(255),lastname varchar(255),phoneNumber number(12))")
# 	a = cursor.execute("DESCRIBE TestDB")
# 	print(a)
# 	return connection.version

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)