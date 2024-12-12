from key_sdk.client import RSAKeyClient
from key_sdk.client import AESKeyClient


if __name__ == '__main__':

    # AES测试示例
    kwargs = {
        'host': 'http://192.168.18.61:9094',
        'app_name': 'sdk01',
        'app_secret': 'zhAD5kHAzCoYh3hvTWFHYT0o4dvBuqox',
        'aes_key_sid': 'sid-778e71c811b6479a8a4c68aee9b5482d',
        'rsa_private_key_sid': 'sid-c6bd936407e14d1499ec5af05f6aeb02'
    }
    # 要加密的明文
    plaintext = b'\x80\xbd\x81=\xb9\xcf(\xc0eI\xe8\x1de\xf4\xc2\x1b\\|gVh\xe73\xa4\r\x97\xb2\xe1f\x90(\x88'
    aes_key_client = AESKeyClient(**kwargs)
    ciphertext = aes_key_client.encrypt(plaintext)
    print("Ciphertext:", ciphertext)
    decrypted_text = aes_key_client.decrypt(ciphertext)
    print("Decrypted Text:", decrypted_text)

    # RSA测试示例
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnF/sNhKJKEEYikJnW/qH
eAvnRmZFKYwyOR+2j0j40/FZV6nb1uYziwTFUDGGDGIvFpGkQB0swH+0vbZkC8Of
sjx4xfZ3eKvHzNSu47WzqQZxRKzQT4Pbw7q3Epli8GWhvehWNO1DmbZZZaa5nK4F
cNCqysI8Uoc3Pef0xGOkkbyvD6yQzOG99dEBzwLjTT6k9UKUESc/rfSrUFkPG+Tc
eJhdX6XowdMA9Ne5T/u2kYJo6+gPQqmyCbgcMWCD4Z12vrKYeVRUSEvIvv71fq+g
bhW+q923WoTg9RXYb2ZelWTDi4t06aQ0JpldnetEw5C5kGv3bKPr8tWncqASBUsB
7wIDAQAB
-----END PUBLIC KEY-----"""
    # 要加密的明文
    plaintext = b'\x80\xbd\x81=\xb9\xcf(\xc0eI\xe8\x1de\xf4\xc2\x1b\\|gVh\xe73\xa4\r\x97\xb2\xe1f\x90(\x88'
    rsa_key_client = RSAKeyClient(**kwargs)
    rsa_key_client.rsa_client.public_key = public_key  # 如果不需要RSA公钥加密，则忽略这一步
    ciphertext = rsa_key_client.encrypt(plaintext)
    print("Ciphertext :", ciphertext)
    decrypted_text = rsa_key_client.decrypt(ciphertext)
    print("Decrypted Text:", decrypted_text)

