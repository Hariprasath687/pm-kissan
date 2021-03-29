from argon2 import PasswordHasher
import json
import AESCipher
import xlsxwriter
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
	workbook = xlsxwriter.Workbook('aadhar_data_insert.xlsx')
	worksheet = workbook.add_worksheet()
	#oracle_writer.write("INSERT INTO AADHAAR_DEMO (AADHAAR_NO, FIRST_NAME, LAST_NAME, FATHER_NAME, GENDER, MOBILE_NO, STATE, DISTRICT, SUB_DISTRICT, BLOCK, VILLAGE, PINCODE, DOB) VALUES")
	worksheet.write("A1", "AADHAAR_NO")
	worksheet.write("B1", "FIRST_NAME")
	worksheet.write("C1", "LAST_NAME")
	worksheet.write("D1", "FATHER_NAME")
	worksheet.write("E1", "GENDER")
	worksheet.write("F1", "MOBILE_NO")
	worksheet.write("G1", "STATE")
	worksheet.write("H1", "DISTRICT")
	worksheet.write("I1", "SUB_DISTRICT")
	worksheet.write("J1", "BLOCK")
	worksheet.write("K1", "VILLAGE")
	worksheet.write("L1", "PINCODE")
	worksheet.write("M1", "DOB")
	for idx,data in enumerate(processed_json_data):
		encrypted_aadhaar = str(data["AADHAAR_NO"]),
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
		worksheet.write("A" + str(idx+1), str(encrypted_aadhaar))
		worksheet.write("B" + str(idx+1), str(encrypted_first_name))
		worksheet.write("C" + str(idx+1), str(encrypted_last_name))
		worksheet.write("D" + str(idx+1), str(encrypted_father_name))
		worksheet.write("E" + str(idx+1), str(encrypted_gender))
		worksheet.write("F" + str(idx+1), str(encrypted_phone))
		worksheet.write("G" + str(idx+1), str(encrypted_state))
		worksheet.write("H" + str(idx+1), str(encrypted_district))
		worksheet.write("I" + str(idx+1), str(encrypted_sub_district))
		worksheet.write("J" + str(idx+1), str(encrypted_block))
		worksheet.write("K" + str(idx+1), str(encrypted_village))
		worksheet.write("L" + str(idx+1), str(encrypted_pincode))
		worksheet.write("M" + str(idx+1), str(encrypted_dob))
	workbook.close()


def generateLandAdmin():
	pass
if givenIp == 1:
	hashPWD()
elif givenIp == 2:
	generateAadhar()
else:
	print("not implemented!")
