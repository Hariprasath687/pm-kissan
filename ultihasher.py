from argon2 import PasswordHasher
ph = PasswordHasher()

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

if givenIp == 1:
	hashPWD()
else:
	print("not implemented!")
