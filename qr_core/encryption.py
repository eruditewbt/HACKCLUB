from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()