from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import pickle
import os

def get_key_path(filename="aes_key.pem"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(current_dir, filename)
    return key_path

def get_key(filename=get_key_path()):
    f = open(filename, mode="rb")
    # Reading file data with read() method
    key = f.read()
    return key

def create_cipher(key, mode=AES.MODE_CBC):
    return AES.new(key, mode)
def get_result_str(cipher, ct_bytes):
    return cipher.iv.hex()+' '+ct_bytes.hex()
def validate_format(ciphertext):
    if (isinstance(ciphertext, str)):
        if(len(ciphertext.split())==2):
            return True  
    return False
def iv_ct_from_result(result):
    return bytes.fromhex(result.split()[0]), bytes.fromhex(result.split()[1])

def encrypt_dict(data):
    data_bytes=pickle.dumps(data)
    return encrypt(data_bytes)
def decrypt_dict(ciphertext):
    data_bytes=decrypt(ciphertext)
    if data_bytes:
        return pickle.loads(data_bytes)
    return None

def encrypt(plaintext):
    key=get_key()
    cipher = create_cipher(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    result = get_result_str(cipher, ct_bytes)
    return result

def decrypt_int(ciphertext):
    key=get_key()
    if validate_format(ciphertext):
        iv,ct=iv_ct_from_result(ciphertext)
        try: 
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            int_val = int.from_bytes(pt, "big")
            return int_val
        # except (ValueError, KeyError):
        #     print("Incorrect decryption")
        except Exception as e:
            return ''
    return ''
    
def decrypt(ciphertext):
    key=get_key()
    if validate_format(ciphertext):
        iv,ct=iv_ct_from_result(ciphertext)
        try: 
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt 
        # except (ValueError, KeyError):
        #     print("Incorrect decryption")
        except Exception as e:
            print(e)
            return b''
    return b''

if __name__ == "__main__":
    data = {"emp_id":1}
    result = encrypt_dict(data)
    print("result", result)