from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from flask.globals import session
from flask.helpers import url_for
import requests
import AESCipher
import cx_Oracle
import fingerprint
import random
import json
from argon2 import PasswordHasher

app = Flask(__name__)
ph = PasswordHasher()
app.secret_key = "RGAGDGYU@719319788*@&@&@,,.s"
connection = cx_Oracle.connect("project","project")
secret_pwd = "Hanover Karens Allover place"
currentSecureOTP = 0

# Setting the json data from file
jsonfile = ""
with open("rawdata.json", "r", encoding="utf-8") as js:
	jsonfile = json.load(js)

with open("config.json", "r", encoding="utf-8") as config:
	server_config = json.load(config)

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
	_request_data = request.json
	print(_request_data)
	print(len(request.form))
	print(request.get_json())
	le_firstname = _request_data["firstname"]
	le_lastname = _request_data["lastname"]
	le_fatherfirstname = _request_data["fatherfirstname"]
	le_fatherlastname = _request_data["fatherlastname"]
	le_dob = _request_data["dob"]
	le_gender = _request_data["gender"]
	print(le_gender)
	le_category = _request_data["category"]
	le_state = _request_data["state"]
	le_district = _request_data["district"]
	le_subdistrict = _request_data["subdistrict"]
	le_block = _request_data["block"]
	le_village = _request_data["village"]
	le_aadhar_number = _request_data["aadhaar"]
	le_smartcard = _request_data["smartcard"]
	le_phoneno = _request_data["phoneno"]
	le_pincode = _request_data["pincode"]
	le_fatherFull = le_fatherfirstname + " " + le_fatherlastname
	cursor = connection.cursor()
	cx = cursor.execute("SELECT * from aadhaar_demo")
	for enc_data in cx:
		aadhaar_enc = enc_data[0]
		firstname_enc = enc_data[1]
		lastname_enc = enc_data[2]
		fathername_enc = enc_data[3]
		gender_enc = enc_data[4]
		mobile_enc = enc_data[5]
		state_enc = enc_data[6]
		district_enc = enc_data[7]
		sub_dist_enc = enc_data[8]
		block_enc = enc_data[9]
		dob_enc = enc_data[10]
		village_enc = enc_data[11]
		pincode_enc = enc_data[12]
		# Data from database
		aadhaar_dec = AESCipher.decrypt(json.loads(aadhaar_enc), password=secret_pwd)
		firstname_dec = AESCipher.decrypt(json.loads(firstname_enc), password=secret_pwd)
		lastname_dec = AESCipher.decrypt(json.loads(lastname_enc), password=secret_pwd)
		fathername_dec = AESCipher.decrypt(json.loads(fathername_enc), password=secret_pwd)
		gender_dec = AESCipher.decrypt(json.loads(gender_enc), password=secret_pwd)
		mobile_dec = AESCipher.decrypt(json.loads(mobile_enc), password=secret_pwd)
		state_dec = AESCipher.decrypt(json.loads(state_enc), password=secret_pwd)
		district_dec = AESCipher.decrypt(json.loads(district_enc), password=secret_pwd)
		sub_dist_dec = AESCipher.decrypt(json.loads(sub_dist_enc), password=secret_pwd)
		block_dec = AESCipher.decrypt(json.loads(block_enc), password=secret_pwd)
		dob_dec = AESCipher.decrypt(json.loads(dob_enc), password=secret_pwd)
		village_dec = AESCipher.decrypt(json.loads(village_enc), password=secret_pwd)
		pincode_dec = AESCipher.decrypt(json.loads(pincode_enc), password=secret_pwd)
		print("Aadhaar :")
		print(le_aadhar_number == str(aadhaar_dec.decode("utf-8")))
		print("Firstname")
		print(str(le_firstname).lower() == str(firstname_dec.decode("utf-8")).lower())
		print("LastName")
		print(str(le_lastname).lower() == str(lastname_dec.decode("utf-8")).lower())
		print("DOB")
		print(str(le_dob).lower() == str(dob_dec.decode("utf-8")).lower())
		print("Gender")
		print(str(le_gender).lower() == str(gender_dec.decode("utf-8")).lower())
		print("State")
		print(str(le_state).lower() == str(state_dec.decode("utf-8")).lower())
		print("District")
		print(str(le_district).lower() == str(district_dec.decode("utf-8")).lower())
		print("SubDistrict")
		print(str(le_subdistrict).lower() ==str(sub_dist_dec.decode("utf-8")).lower())
		print("Block")
		print(str(le_block).lower() == str(block_dec.decode("utf-8")).lower())
		print("Village")
		print(str(le_village).lower() == str(village_dec.decode("utf-8")).lower())
		print("Pincode")
		print(str(le_pincode).lower() == str(pincode_dec.decode("utf-8")).lower())
		if (le_aadhar_number == str(aadhaar_dec.decode("utf-8")) and
			str(le_firstname).lower() == str(firstname_dec.decode("utf-8")).lower() and
			str(le_lastname).lower() == str(lastname_dec.decode("utf-8")).lower() and
			str(le_dob).lower() == str(dob_dec.decode("utf-8")).lower() and
			str(le_gender).lower() == str(gender_dec.decode("utf-8")).lower() and
			# str(le_state).lower() == str(state_dec.decode("utf-8")).lower() and
			# str(le_district).lower() == str(district_dec.decode("utf-8")).lower() and
			str(le_subdistrict).lower() ==str(sub_dist_dec.decode("utf-8")).lower() and
			str(le_block).lower() == str(block_dec.decode("utf-8")).lower() and
			str(le_village).lower() == str(village_dec.decode("utf-8")).lower() and
			str(le_pincode).lower() == str(pincode_dec.decode("utf-8")).lower()):
			getRandomData()
			smsApiResponse = requests.post(
				server_config["base_url"],
				headers={
					"Content-Type": "application/json",
					"authorization": server_config["api_token"]
				},
				json={
					"route" : "q",
					"message" : "Your PM-KISAN 8 Digit OTP is {}".format(currentSecureOTP),
					"language" : "english",
					"flash" : 0,
					"numbers" : "8825955792"
				}
			)
			jsonApiResponse = smsApiResponse.json()
			print(jsonApiResponse)
			if jsonApiResponse["return"]:
				return jsonify({"result": "message sent!"})
			else:
				return jsonify({"result": "message not sent!"})
		else:
			return jsonify({"result": "Not valid"})

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

@app.route('/verifyTOTP', methods=['POST'])
def verify_totp():
	otp = request.json["otp"]
	print("otp sent from {}".format(otp))
	print("otp stored : {}".format(currentSecureOTP))
	if otp == str(currentSecureOTP):
		return jsonify({"result": "ok"})
	else:
		return jsonify({"result": "not ok"})

def getRandomData():
	global currentSecureOTP
	currentSecureOTP = random.randint(12345678, 99999999)
	return currentSecureOTP


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