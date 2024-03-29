from base64 import b64decode, b64encode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import json


def decrypt(enc_dict, password):
	# decode the dictionary entries from base64
	salt = b64decode(enc_dict['salt'])
	cipher_text = b64decode(enc_dict['cipher_text'])
	nonce = b64decode(enc_dict['nonce'])
	tag = b64decode(enc_dict['tag'])
	

	# generate the private key from the password and salt
	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

	# create the cipher config
	cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

	# decrypt the cipher text
	decrypted = cipher.decrypt_and_verify(cipher_text, tag)

	return decrypted

def encrypt(plain_text, password):
	# generate a random salt
	salt = get_random_bytes(AES.block_size)
	
	# use the Scrypt KDF to get a private key from the password
	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
	print("Using " + str(len(private_key) * 8) + " Bits key for encrypting data")
	# create cipher config
	cipher_config = AES.new(private_key, AES.MODE_GCM)

	# return a dictionary with the encrypted text
	cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
	encryted_data = {
		'cipher_text': b64encode(cipher_text).decode('utf-8'),
		'salt': b64encode(salt).decode('utf-8'),
		'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
		'tag': b64encode(tag).decode('utf-8')
	}
	return json.dumps(encryted_data)

if __name__ == "__main__":
	while True:
			secret_key = "A@fa.ada281001--1=XAxeE"
			data_to_encrypt = input("Enter the data to encrypt! :")
			encrypted_data = encrypt(data_to_encrypt, secret_key)
			print(encrypted_data)
			print('data')
			lame_data = input()
			decrypted = decrypt(json.loads('{"cipher_text": "nWwgKz29", "salt": "ZcN4IHyHZw9LyTWMypz6aA==", "nonce": "MtY+vMLU8/R5WPoCZt/cfQ==", "tag": "8fHNMqYeqCZmziyV5dV7Nw=="}'), "Hanover Karens Allover place")
			print(decrypted.decode("utf-8"))
