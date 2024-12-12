# keyvault_sdk

密钥管理Python SDK

## 使用示例

### 安装sdk
```bash
pip install keyvault-sdk
```
### AES
```bash
from key_sdk.client import AESKeyClient
# AES测试示例
kwargs = {
    'host': 'http://127.0.0.1:9094',
    'app_name': 'test',
    'app_secret': '1111111111111',
    'aes_key_sid': 'sid-xxxxxxxxxxxxxxx',
}
# 要加密的明文
plaintext = b'\x80\xbd\x81=\xb9\xcf(\xc0eI\xe8\x1de\xf4\xc2\x1b\\|gVh\xe73\xa4\r\x97\xb2\xe1f\x90(\x88'
aes_key_client = AESKeyClient(**kwargs)
ciphertext_base64 = aes_key_client.encrypt(plaintext)
print("Ciphertext (Base64):", ciphertext_base64)
decrypted_text = aes_key_client.decrypt(ciphertext_base64)
print("Decrypted Text:", decrypted_text)
```

### RSA
```bash
from key_sdk.client import RSAKeyClient
# RSA测试示例
kwargs = {
    'host': 'http://127.0.0.1:9094',
    'app_name': 'test',
    'app_secret': '1111111111111',
    'rsa_private_key_sid': 'sid-yyyyyyyyyyyyy',
}
public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArg4ZTp1AhXY9LJ01nNDd
lST/JaNnG7Ne+9x6XCzwmwkXRzAQbKGgygBqlTdfqqdT+rwwa2FEeebxw4JuiMsl
XapUvYCxrPSdQB3ItH7Gm4rzaCrs6nXjhZozHUEYEP2+ylb77QxW+FwBr0aMuo6q
M2qsyk2nTN5Y7Kq2gsIyQcwAsRQpJk9+oUvrYbWZwjFo/l2ilJI1MKY9N5lJ/FUR
olCkVkKqXyHm2+fpnLCjnJKZS54idkiQzomE85VbGUw7ZDjl3k6NwLC+2Mt4qgFx
Z5ElOAkXdG1S3xCy466uNyw1fr+8QnkyCRwJuIr5Ww5v8njbzwV/FiednELat8oY
uQIDAQAB
-----END PUBLIC KEY-----"""
# 要加密的明文
plaintext = b'\x80\xbd\x81=\xb9\xcf(\xc0eI\xe8\x1de\xf4\xc2\x1b\\|gVh\xe73\xa4\r\x97\xb2\xe1f\x90(\x88'
rsa_key_client = RSAKeyClient(**kwargs)
rsa_key_client.rsa_client.public_key = public_key  # 如果不需要RSA公钥加密，则忽略这一步
ciphertext_base64 = rsa_key_client.encrypt(plaintext)
print("Ciphertext (Base64):", ciphertext_base64)
decrypted_text = rsa_key_client.decrypt(ciphertext_base64)
print("Decrypted Text:", decrypted_text)
```