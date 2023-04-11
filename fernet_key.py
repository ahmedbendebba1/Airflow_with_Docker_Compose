from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
#vQ0ru_QwhOH_HhCRRj5byg8el8eAeH9_BpiId3g52P8=