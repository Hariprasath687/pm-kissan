from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from flask.globals import session
from flask.helpers import url_for
import requests
import cx_Oracle
import json
from argon2 import PasswordHasher
import ctypes
from ctypes import wintypes

app = Flask(__name__)
ph = PasswordHasher()
app.secret_key = "RGAGDGYU@719319788*@&@&@,,.s"

# Setting the json data from file
jsonfile = ""
with open("rawdata.json", "r", encoding="utf-8") as js:
	jsonfile = json.load(js)

# connection = cx_Oracle.connect("project","project")




SECURITY_MAX_SID_SIZE = 68
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_ID_TYPE_SID = 3

# Error Info
WINBIO_E_NO_MATCH = 0x80098005

lib = ctypes.WinDLL(r"C:\Windows\System32\winbio.dll")


class GUID(ctypes.Structure):
	_fields_ = [("Data1", wintypes.DWORD),
				("Data2", wintypes.WORD),
				("Data3", wintypes.WORD),
				("Data4", wintypes.BYTE * 8)
				]


class AccountSid(ctypes.Structure):
	_fields_ = [("Size", wintypes.ULONG),
				("Data", ctypes.c_ubyte * SECURITY_MAX_SID_SIZE)
				]


class Value(ctypes.Union):
	_fields_ = [("NULL", wintypes.ULONG),
				("Wildcard", wintypes.ULONG),
				("TemplateGuid", GUID),
				("AccountSid", AccountSid)
				]


class WINBIO_IDENTITY(ctypes.Structure):
	_fields_ = [("Type", ctypes.c_uint32),
				("Value", Value)]


class TOKEN_INFORMATION_CLASS:
	TokenUser = 1
	TokenGroups = 2
	TokenPrivileges = 3


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
	_fields_ = [("Value", wintypes.BYTE*6)]


# https://www.csie.ntu.edu.tw/~r92094/c++/Win_Header/WINNT.H
class SID(ctypes.Structure):
	_fields_ = [("Revision", wintypes.BYTE),
				("SubAuthorityCount", wintypes.BYTE),
				("IdentifierAuthority", SID_IDENTIFIER_AUTHORITY),
				("SubAuthority", wintypes.DWORD)]


class SID_AND_ATTRIBUTES(ctypes.Structure):
	_fields_ = [("Sid", ctypes.POINTER(SID)),
				("Attributes", wintypes.DWORD)]


class TOEKN_USER(ctypes.Structure):
	_fields_ = [("User", SID_AND_ATTRIBUTES)]


class FingerPrint:
	def __init__(self):
		self.session_handle = ctypes.c_uint32()
		self.unit_id = ctypes.c_uint32()

		# important  represent which finger you are using
		# full definition is in winbio_types.h
		self.subfactor = ctypes.c_ubyte(0xf5)       # WINBIO_FINGER_UNSPECIFIED_POS_01

		# WINBIO_ID_TYPE_SID = 3
		self.identity = WINBIO_IDENTITY()
		self.IsOpen = False

	def open(self):
		if self.IsOpen:
			return
		ret = lib.WinBioOpenSession(WINBIO_TYPE_FINGERPRINT,  # finger print
									WINBIO_POOL_SYSTEM,
									WINBIO_FLAG_DEFAULT,
									None,
									0,
									None,
									ctypes.byref(self.session_handle))  # pool   system
		if ret & 0xffffffff != 0x0:
			print("Open Failed!")
			return False
		self.IsOpen = True
		return True

	def locate_unit(self):
		ret = lib.WinBioLocateSensor(self.session_handle, ctypes.byref(self.unit_id))
		print(self.unit_id)
		if ret & 0xffffffff != 0x0:
			print("Locate Failed!")
			return False
		return True

	def identify(self):
		reject_detail = ctypes.c_uint32()
		ret = lib.WinBioIdentify(self.session_handle, ctypes.byref(self.unit_id), ctypes.byref(self.identity),
								 ctypes.byref(self.subfactor),
								 ctypes.byref(reject_detail))
		if ret & 0xffffffff != 0x0:
			print(hex(ret & 0xffffffff))
			raise Exception("Identify Error")
		print(f"Unit ID\t:{hex(self.unit_id.value)}")
		print(f"Sub Factor\t:{hex(self.subfactor.value)}")
		print(f"Identity Type\t: {self.identity.Type}")
		print(f"Identity AccountSid Data\t: {list(self.identity.Value.AccountSid.Data)[0:self.identity.Value.AccountSid.Size]}")
		print(f"Identity AccountSid Size\t: {self.identity.Value.AccountSid.Size}")
		print(f"Rejected Details:\t{hex(reject_detail.value)}")

	def verify(self):
		match = ctypes.c_bool(0)
		reject_detail = ctypes.c_uint32()
		# get identity
		self.get_current_user_identity()
		ret = lib.WinBioVerify(self.session_handle, ctypes.byref(self.identity),
							   self.subfactor, ctypes.byref(self.subfactor),
							   ctypes.byref(match), ctypes.byref(reject_detail))
		if ret & 0xffffffff == WINBIO_E_NO_MATCH or ret & 0xffffffff == 0:
			return match.value
		else:
			print(hex(ret & 0xffffffff))
			raise Exception("Identify Error")

	def close(self):
		if not self.IsOpen:
			return
		lib.WinBioCloseSession(self.session_handle)
		self.session_handle = 0

	def get_current_user_identity(self):
		self.get_token_information()

	@staticmethod
	def get_process_token():
		"""
		Get the current process token
		"""
		#  Reference
		#  https://gist.github.com/schlamar/7024668
		GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
		GetCurrentProcess.restype = wintypes.HANDLE
		OpenProcessToken = ctypes.windll.advapi32.OpenProcessToken
		OpenProcessToken.argtypes = (wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE))
		OpenProcessToken.restype = wintypes.BOOL
		token = wintypes.HANDLE()

		# https://github.com/Alexpux/mingw-w64/blob/master/mingw-w64-tools/widl/include/winnt.h
		# TOKEN_READ = STANDARD_RIGHTS_READ | TOKEN_QUERY = 0x00020000 | 0x0008 = 0x20008
		# TOKEN_ALL_ACCESS = 0xf01ff

		TOKEN_READ = 0x20008
		res = OpenProcessToken(GetCurrentProcess(), TOKEN_READ, token)
		if not res > 0:
			raise RuntimeError("Couldn't get process token")
		return token

	def get_token_information(self):
		"""
		Get token info associated with the current process.
		"""
		GetTokenInformation = ctypes.windll.advapi32.GetTokenInformation
		GetTokenInformation.argtypes = [
			wintypes.HANDLE,  # TokenHandle
			ctypes.c_uint,  # TOKEN_INFORMATION_CLASS value
			wintypes.LPVOID,  # TokenInformation
			wintypes.DWORD,  # TokenInformationLength
			ctypes.POINTER(wintypes.DWORD),  # ReturnLength
			]
		GetTokenInformation.restype = wintypes.BOOL

		CopySid = ctypes.windll.advapi32.CopySid
		CopySid.argtypes = [
			wintypes.DWORD,     # nDestinationSidLength
			ctypes.c_void_p,    # pDestinationSid,
			ctypes.c_void_p     # pSourceSid
		]
		CopySid.restype = wintypes.BOOL

		GetLengthSid = ctypes.windll.advapi32.GetLengthSid
		GetLengthSid.argtypes = [
			ctypes.POINTER(SID)  # PSID
		]
		GetLengthSid.restype = wintypes.DWORD

		return_length = wintypes.DWORD(0)
		buffer = ctypes.create_string_buffer(SECURITY_MAX_SID_SIZE)

		res = GetTokenInformation(self.get_process_token(),
								  TOKEN_INFORMATION_CLASS.TokenUser,
								  buffer,
								  SECURITY_MAX_SID_SIZE,
								  ctypes.byref(return_length)
								  )
		assert res > 0, "Error in second GetTokenInformation (%d)" % res

		token_user = ctypes.cast(buffer, ctypes.POINTER(TOEKN_USER)).contents
		CopySid(SECURITY_MAX_SID_SIZE,
				self.identity.Value.AccountSid.Data,
				token_user.User.Sid
				)
		self.identity.Type = WINBIO_ID_TYPE_SID
		self.identity.Value.AccountSid.Size = GetLengthSid(token_user.User.Sid)





# Routes for our page comes here #
@app.route('/')
def index():
	if session["username"]:
		return render_template('dashboard.html')
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/login')
def login():
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

@app.route('/admin', methods=["POST"])
def admin_route():
	user = session["username"]
	return render_template("dashboard.html", username= user)

@app.route('/fingerpintverify', methods=["POST"])
def verifyFingerprint():
	print("getting req")
	myFP = FingerPrint()
	try:
		myFP.open()
		print("Please touch the fingerprint sensor")
		if myFP.verify():
			print("Hello! Master")
			print("Verified")
			return redirect(url_for(".admin_route"), 307)
		else:
			print("Sorry! Man")
			return jsonify({"authorizedUser": "false"})
	finally:
		myFP.close()		

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