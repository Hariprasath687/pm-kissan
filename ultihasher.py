from argon2 import PasswordHasher
import json
import AESCipher
ph = PasswordHasher()
secret_pwd = "Hanover Karens Allover place"
print("1.Hash Passwords\n2.Aadhaar data\n3.PM Kissan\n4.Land database\n5.exit")

givenIp = int(input("Option :"))

def hashPWD():
	op = int(input("1.Hash\n2.Verify\n3.rehash?"))
	if op == 1:
		passwrd = input("Enter the password you need to encrypt :")
		print(ph.hash(passwrd))
	elif op == 2:
		password = input("Enter the password to verify! :")
		hashVal = input("Enter the hash for that password! :")
		try:
			if ph.verify(hashVal, password):
				print("Verified, they match!!\n")
			else:
				print("Failed!")
		except:
			print("Something went wrong")
	elif op == 3:
		RehashVal = input("Enter the hash for that Checking! :")
		print(ph.check_needs_rehash(RehashVal))
	else:
		print("Veliya po da")
		
def generateAadhar():
	with open("aadhar_data.json", 'r', encoding="utf-8") as f:
		jsonfile = json.load(f)
	processed_json_data = jsonfile
	oracle_writer = open("aadhar_data_insert.txt", "a+", encoding="utf-8")
	for data in processed_json_data:
		encrypted_aadhaar = AESCipher.encrypt(str(data["AADHAAR_NO"]), secret_pwd)
		encrypted_first_name = AESCipher.encrypt(data["FIRST_NAME"], secret_pwd)
		encrypted_last_name = AESCipher.encrypt(data["LAST_NAME"], secret_pwd)
		encrypted_father_name = AESCipher.encrypt(data["FATHER_NAME"], secret_pwd)
		encrypted_gender = AESCipher.encrypt(data["GENDER"], secret_pwd)
		encrypted_phone = AESCipher.encrypt(data["MOBILE_NO"], secret_pwd)
		encrypted_state = AESCipher.encrypt(data["STATE"], secret_pwd)
		encrypted_district = AESCipher.encrypt(data["DISTRICT"], secret_pwd)
		encrypted_sub_district = AESCipher.encrypt(data["SUB_DISTRICT"], secret_pwd)
		encrypted_block = AESCipher.encrypt(data["BLOCK"], secret_pwd)
		encrypted_dob = AESCipher.encrypt(data["DOB"], secret_pwd)
		encrypted_village = AESCipher.encrypt(data["VILLAGE"], secret_pwd)
		encrypted_pincode = AESCipher.encrypt(str(data["PINCODE"]), secret_pwd)
		encrypted_isEligible = AESCipher.encrypt(data["isEligible"], secret_pwd)
		# 
		oracle_writer.write("INSERT INTO AADHAAR_DEMO (AADHAAR_NO, FIRST_NAME, LAST_NAME, GENDER, MOBILE_NO, STATE, DISTRICT, SUB_DISTRICT, BLOCK, VILLAGE, PINCODE, DOB, Eligiblity) VALUES")
		oracle_writer.write("('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"
			.format(
					encrypted_aadhaar,
					encrypted_first_name,
					encrypted_last_name,
					encrypted_father_name,
					encrypted_gender,
					encrypted_phone,
					encrypted_state,
					encrypted_district,
					encrypted_sub_district,
					encrypted_block,
					encrypted_dob,
					encrypted_village,
					encrypted_pincode,
					encrypted_isEligible
				)
			)
		oracle_writer.write(";")
	oracle_writer.close()

if givenIp == 1:
	hashPWD()
elif givenIp == 2:
	generateAadhar()
else:
	print("not implemented!")
