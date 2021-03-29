from Cryptodome.Cipher import AES
from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from flask.globals import session
from flask.helpers import url_for
from argon2 import PasswordHasher
import requests
import AESCipher
import cx_Oracle
import fingerprint
import random
import json
import datetime

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
	cx = cursor.execute("SELECT * from aadhaar_demo where AADHAAR_NO={}".format(le_aadhar_number))
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
		village_enc = enc_data[10]
		pincode_enc = enc_data[11]
		dob_enc = enc_data[12]
		# Data from database
		aadhaar_dec = aadhaar_enc
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
		print(le_aadhar_number == le_aadhar_number)
		print("Firstname")
		print(str(le_firstname).lower() == str(firstname_dec.decode("utf-8")).lower())
		print("LastName")
		print(str(le_lastname).lower() == str(lastname_dec.decode("utf-8")).lower())
		print("FatherName:")
		print(str(le_fatherFull).lower()  == str(fathername_dec.decode("utf-8")).lower())
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
		print(le_pincode)
		print(str(pincode_dec.decode("utf-8")).lower())
		if (le_aadhar_number == le_aadhar_number and
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

@app.route('/verify_land', methods=['POST'])
def verifyLandDb():
	userData = request.json
	landstate = userData["landstate"]
	landDist = userData["landDist"]
	landtypearea = userData["landtypearea"]
	taluk = userData["taluk"]
	landvillage = userData["landvillage"]
	ownerName = userData["ownerName"]
	wardNumber = userData["wardNumber"]
	blockNumber = userData["blockNumber"]
	dataland = userData["dataland"]
	land_uid = ""
	if landtypearea == "rural":
		land_uid = landstate[0:3].lower() + landDist[0:3].lower() + taluk[0:3].lower() + "r" + landvillage[0:3].lower() + dataland[0]["patta"].lower() + dataland[0]["survey"].lower() + dataland[0]["subdivison"].lower()
	else:
		land_uid = landstate[0:3].lower() + landDist[0:3].lower() + taluk[0:3].lower() + "u" + wardNumber.lower() + blockNumber.lower() + dataland[0]["patta"].lower() + dataland[0]["survey"].lower() + dataland[0]["subdivison"].lower()
	cursor = connection.cursor()
	la_find_querry = "SELECT * from land_admin where LAND_UID={}".format(land_uid)
	cx = cursor.execute(la_find_querry)
	for data in cx:
		encr_state = data[0]
		encr_dist = data[1]
		encr_taluk = data[2]
		encr_area_type = data[3]
		encr_village = data[4]
		encr_ward = data[5]
		encr_block = data[6]
		encr_owner = data[7]
		encr_patta = data[8]
		encr_survey = data[9]
		encr_subdiv = data[10]
		encr_land_type = data[11]
		encr_area = data[12]
		# decrypting the land db
		dec_state = AESCipher.decrypt(encr_state, secret_pwd)
		dec_dist = AESCipher.decrypt(encr_dist, secret_pwd)
		dec_taluk = AESCipher.decrypt(encr_taluk, secret_pwd)
		dec_area_type = AESCipher.decrypt(encr_area_type, secret_pwd)
		dec_village = AESCipher.decrypt(encr_village, secret_pwd)
		dec_ward = AESCipher.decrypt(encr_ward, secret_pwd)
		dec_block = AESCipher.decrypt(encr_block, secret_pwd)
		dec_owner = AESCipher.decrypt(encr_owner, secret_pwd)
		dec_patta = AESCipher.decrypt(encr_patta, secret_pwd)
		dec_survey = AESCipher.decrypt(encr_survey, secret_pwd)
		dec_subdiv = AESCipher.decrypt(encr_subdiv, secret_pwd)
		dec_land_type = AESCipher.decrypt(encr_land_type, secret_pwd)
		dec_area = AESCipher.decrypt(encr_area, secret_pwd)
		if (
			str(landstate).lower() == str(dec_state.decode("utf-8")).lower() and
			str(landDist).lower() == str(dec_dist.decode("utf-8")).lower() and
			str(taluk).lower() == str(dec_taluk.decode("utf-8")).lower() and
			str(landtypearea).lower() == str(dec_area_type.decode("utf-8")).lower() and
			str(ownerName).lower() == str(dec_owner.decode("utf-8")).lower() and
			str(dataland[0]["patta"]).lower() == str(dec_patta.decode("utf-8")).lower() and
			str(dataland[0]["survey"]).lower() == str(dec_survey.decode("utf-8")).lower() and
			str(dataland[0]["subdivison"]).lower() == str(dec_subdiv.decode("utf-8")).lower() and
			str(dataland[0]["isLandType"]).lower() == str(dec_land_type.decode("utf-8")).lower() and
			str(dataland[0]["area"]).lower() == str(dec_area.decode("utf-8")).lower()
		):
			if(str(landtypearea) == "rural"):
				print("Loading Rural database...")
				print(str(landvillage).lower() == str(dec_village.decode("utf-8")).lower())
				if(str(landvillage).lower() == str(dec_village.decode("utf-8")).lower()):
					print("Verified! Land Data")
					return jsonify({"result": "ok"})
				else:
					return jsonify({"result": "no"})
			else:
				print("Loading urban database...")
				print("Ward number check :")
				print(str(wardNumber).lower() == str(dec_ward.decode("utf-8")).lower())
				print("Block number check :")
				print(str(blockNumber).lower() == str(dec_block.decode("utf-8")).lower())
				if (str(wardNumber).lower() == str(dec_ward.decode("utf-8")).lower() 
					and str(blockNumber).lower() == str(dec_block.decode("utf-8")).lower()):
					print("Verified! Land Data")
					return jsonify({"result": "ok"})
				else:
					return jsonify({"result": "no"})
		else:
			return jsonify({"result": "no"})

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
		ownerName,
		wardNumber,
		blockNumber,
		stringified_dataland
		)
	# WRAP UP WITH STR
	enc_firstname = str(AESCipher.encrypt(firstName, secret_pwd))
	enc_lastname = str(AESCipher.encrypt(lastName, secret_pwd))
	enc_fatherName = str(AESCipher.encrypt(fatherName, secret_pwd))
	enc_dob = str(AESCipher.encrypt(dob, secret_pwd))
	enc_gender = str(AESCipher.encrypt(gender, secret_pwd))
	enc_category = str(AESCipher.encrypt(category, secret_pwd))
	enc_district = str(AESCipher.encrypt(district, secret_pwd))
	enc_subdistrict = str(AESCipher.encrypt(subdistrict, secret_pwd))
	enc_block = str(AESCipher.encrypt(block, secret_pwd))
	enc_state = str(AESCipher.encrypt(state, secret_pwd))
	enc_village = str(AESCipher.encrypt(village, secret_pwd))
	enc_pincode = str(AESCipher.encrypt(pincode, secret_pwd))
	enc_aadhaar = str(AESCipher.encrypt(aadhaar, secret_pwd))
	enc_smartcard = str(AESCipher.encrypt(smartcard, secret_pwd))
	enc_phoneno = str(AESCipher.encrypt(phoneno, secret_pwd))
	enc_bankIFSC = str(AESCipher.encrypt(bankIFSC, secret_pwd))
	enc_bankName = str(AESCipher.encrypt(bankName, secret_pwd))
	enc_bankAccNumber = str(AESCipher.encrypt(bankAccNumber, secret_pwd))
	enc_bankAccName = str(AESCipher.encrypt(bankAccName, secret_pwd))
	enc_landstate = str(AESCipher.encrypt(landstate, secret_pwd))
	enc_landDist = str(AESCipher.encrypt(landDist, secret_pwd))
	enc_landtypearea = str(AESCipher.encrypt(landtypearea, secret_pwd))
	enc_taluk = str(AESCipher.encrypt(taluk, secret_pwd))
	enc_landvillage = str(AESCipher.encrypt(landvillage, secret_pwd))
	enc_ownerName = str(AESCipher.encrypt(ownerName, secret_pwd))
	enc_wardNumber = str(AESCipher.encrypt(wardNumber, secret_pwd))
	enc_blockNumber = str(AESCipher.encrypt(blockNumber, secret_pwd))
	enc_stringified_dataland = str(AESCipher.encrypt(stringified_dataland, secret_pwd))
	enc_patta_no = str(AESCipher.encrypt(str(dataland[0]["patta"]), secret_pwd))
	enc_survey_no = str(AESCipher.encrypt(str(dataland[0]["survey"]), secret_pwd))
	enc_subdiv_no = str(AESCipher.encrypt(str(dataland[0]["subdivison"]), secret_pwd))
	enc_landType = str(AESCipher.encrypt(str(dataland[0]["isLandType"]), secret_pwd))
	enc_area = str(AESCipher.encrypt(str(dataland[0]["area"]), secret_pwd))
	land_uid = ""
	if landtypearea == "rural":
		land_uid = landstate[0:3] + landDist[0:3] + district[0:3] + taluk[0:3] + "R" + landvillage[0:3] + dataland[0]["patta"] + dataland[0]["survey"] + dataland[0]["subdivison"]
	else:
		land_uid = landstate[0:3] + landDist[0:3] + district[0:3] + taluk[0:3] + "U" + wardNumber + blockNumber + dataland[0]["patta"] + dataland[0]["survey"] + dataland[0]["subdivison"]
	cursor = connection.cursor()
	currentPMKisan = generatePMKisanId()
	pmk_insert_query = "Insert into PM_KISAN_PERSONAL values({}, {}, {}, {},{}, {}, {}, {}, {}, {}, {}, {},{}, {}, {}, {}, {})".format(
		currentPMKisan,
		enc_firstname,
		enc_lastname,
		enc_fatherName,
		enc_dob,
		enc_gender,
		enc_category,
		enc_state,
		enc_district,
		enc_subdistrict,
		enc_block,
		enc_village,
		enc_pincode,
		enc_aadhaar,
		enc_smartcard,
		enc_phoneno,
		"submitted"
	)
	pmb_insert_query = "Insert into pm_kisan_Bank values({}, {}, {}, {}, {})".format(
		currentPMKisan,
		enc_bankName,
		enc_bankIFSC,
		enc_bankAccNumber,
		enc_bankAccName
	)
	pml_insert_query = "Insert into pm_kisan_land values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
		currentPMKisan,
		enc_landstate,
		enc_landDist,
		enc_taluk,
		enc_landtypearea,
		enc_landvillage,
		enc_wardNumber,
		enc_blockNumber,
		enc_ownerName,
		enc_patta_no,
		enc_survey_no,
		enc_subdiv_no,
		enc_landType,
		enc_area
	)
	cursor.execute(pmk_insert_query)
	cursor.execute(pmb_insert_query)
	cursor.execute(pml_insert_query)
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

def generatePMKisanId():
	return "PMK{}".format(str(datetime.datetime.now().timestamp()).replace(".",""))

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