import hashlib
from django.db import DatabaseError, connections, models, connection
from django.db.models import Func
from django.conf import settings
from decimal import Decimal

class DatabaseUtils():
    def __init__(self):
        self.connection = connections['sym_keys']
        self.cursor = self.connection.cursor()
    
    @staticmethod
    def get_keys():
        try:
            with connections['sym_keys'].cursor() as cursor:
                cursor.execute(f"SELECT key FROM sym_keys.aes_keys")
                rows = cursor.fetchall()
                keys = [row[0] for row in rows]
            return keys
        except DatabaseError as e:
            print(f"Error while getting keys: {e}")

    @staticmethod
    def save_key(key):
        try:
            with connections['sym_keys'].cursor() as cursor:
                cursor.execute(f"INSERT INTO sym_keys.aes_keys (key, created_at) VALUES (%s, NOW())", [key])
        except DatabaseError as e:
            print(f"Error while saving key: {e}")
            raise DatabaseError(f"Error while saving key: {e}")
    
    @staticmethod
    def calculate_checksum(value):
        if value is not None:
            if isinstance(value, bytes):
                return value  
            checksum = hashlib.sha256(value.encode('utf-8')).hexdigest()
            return checksum
        return None
    
    @staticmethod
    def get_current_schema():
        options = settings.DATABASES['default'].get('OPTIONS', {})
        search_path = options.get('options', '')
        if search_path:
            # Extract schema name from search_path option
            search_path = search_path.split('=')[1].split(',')[0].strip()
            return search_path
        return 'public'  # Default to 'public' schema if not specified

class PgEncrypt():
    def __init__(self, connection_name='sym_keys'):
        self.connection = connections[connection_name]
        self.cursor = self.connection.cursor()
        self.schema = DatabaseUtils.get_current_schema()
        self.all_keys = DatabaseUtils.get_keys()
        self.key = self.all_keys[0] if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
    
    def encrypt_value(self, value):
        if value is not None:            
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value
    
class PgDecrypt():
    def __init__(self, connection_name='sym_keys'):
        self.connection = connections[connection_name]
        self.cursor = self.connection.cursor()
        self.schema = DatabaseUtils.get_current_schema()
        self.all_keys = DatabaseUtils.get_keys()
        self.key = self.all_keys[0] if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY
    
    def decrypt_value(self, value):
        if value is not None:      
            with self.connection.cursor() as cursor:      
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.key])
                result = cursor.fetchone()
                if result:
                    string_value_checksum = result[0]
                    if isinstance(string_value_checksum, memoryview):
                        string_value_checksum = string_value_checksum.tobytes()
                    if isinstance(string_value_checksum, bytes):
                        string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                    value, checksum = string_value_checksum.rsplit("::", 1)
                    checksum_2 = DatabaseUtils.calculate_checksum(value)
                    if checksum_2 == checksum:
                        return value
                    else:
                        raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                else:
                    print(f"\n============================================\nDecryption failed or returned no value.\n============================================\n")
                    return None
        return value
    
class EncryptedTextField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            if isinstance(value, bytes):
                return value
            split = value.split("::")
            if len(split) == 2:
                return value  
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            checksum_2 = DatabaseUtils.calculate_checksum(value)
                            if checksum_2 == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value

class EncryptedCharField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            if isinstance(value, bytes):
                return value
            split = value.split("::")
            if len(split) == 2:
                return value  
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            checksum_2 = DatabaseUtils.calculate_checksum(value)
                            if checksum_2 == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value

class EncryptedEmailField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):        
        if value is not None:
            if isinstance(value, bytes):
                return value
            split = value.split("::")
            if len(split) == 2:
                return value            
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            checksum_2 = DatabaseUtils.calculate_checksum(value)
                            if checksum_2 == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value

class EncryptedIntegerField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):        
        if value is not None:
            if isinstance(value, bytes):
                return value
            split = value.split("::")
            if len(split) == 2:
                return value  
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            checksum_2 = DatabaseUtils.calculate_checksum(value)
                            if checksum_2 == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value

class EncryptedFloatField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            if DatabaseUtils.calculate_checksum(value) == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value

class EncryptedDecimalField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = DatabaseUtils.get_keys()
        self.encrypt_key = self.all_keys[0].strip() if self.all_keys else settings.PGCRYPTO_DEFAULT_KEY.strip()
        self.schema = DatabaseUtils.get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            checksum = DatabaseUtils.calculate_checksum(value)
            value_checksum = f"{value}::{checksum}"
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value_checksum, self.encrypt_key])
                result = cursor.fetchone()
                if result:
                    # Ensure the encrypted value is properly returned
                    encrypted_value = result[0]
                    if isinstance(encrypted_value, memoryview):
                        value = encrypted_value.tobytes()  # Convert memoryview to bytes
                        return value
                    else:
                        return encrypted_value
                else:
                    # Handle the case where encryption returns no value
                    print(f"\n============================================\nEncryption failed or returned no value.\n============================================\n")
                    return None
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                for key in self.all_keys:
                    try:
                        cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, key.strip()])
                        result = cursor.fetchone()
                        if result:
                            string_value_checksum = result[0]
                            if isinstance(string_value_checksum, memoryview):
                                string_value_checksum = string_value_checksum.tobytes()
                            if isinstance(string_value_checksum, bytes):
                                string_value_checksum = string_value_checksum.decode('utf-8')  # Convert bytes to string
                            value, checksum = string_value_checksum.rsplit("::", 1)
                            if DatabaseUtils.calculate_checksum(value) == checksum:
                                return value
                            else:
                                raise ValueError("Checksum mismatch! Data may have been corrupted or tampered with.")
                    except Exception as e:
                        print(f"Decryption with key {key} failed: {e}")
        return value
