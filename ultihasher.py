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
		encrypted_name = AESCipher.encrypt(data["name"], secret_pwd)
		encrypted_gender = AESCipher.encrypt(data["gender"], secret_pwd)
		encrypted_dob = AESCipher.encrypt(data["DOB"], secret_pwd)
		encrypted_father_name = AESCipher.encrypt(data["fatherName"], secret_pwd)
		encrypted_mother_name = AESCipher.encrypt(data["motherName"], secret_pwd)
		encrypted_email = AESCipher.encrypt(data["email"], secret_pwd)
		encrypted_phone = AESCipher.encrypt(data["phone"], secret_pwd)
		encrypted_address = AESCipher.encrypt(data["address"], secret_pwd)
		encrypted_isEligible = AESCipher.encrypt(data["isEligible"], secret_pwd)
		oracle_writer.write("INSERT INTO AadhaarCard (name, gender, DOB, fatherName, motherName, email, phoneNumber, address, Eligiblity) VALUES")
		oracle_writer.write("({}, {}, {}, {}, {}, {}, {}, {} {}".format(encrypted_name, encrypted_gender, encrypted_dob, encrypted_father_name, encrypted_mother_name, encrypted_email, encrypted_phone, encrypted_address, encrypted_isEligible))
		oracle_writer.write(";")
	oracle_writer.close()

if givenIp == 1:
	hashPWD()
elif givenIp == 2:
	generateAadhar()
else:
	print("not implemented!")
