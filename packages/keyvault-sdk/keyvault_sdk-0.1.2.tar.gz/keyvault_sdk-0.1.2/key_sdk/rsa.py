from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from key_sdk.utils import encode16, decode16


class RSAClient(object):
    def __init__(
            self,
            private_key: bytes,
            public_key: bytes = None,
    ):
        # 公钥
        self.public_key = public_key
        # 私钥
        self.private_key = private_key

    def encrypt(self, plaintext):
        # 加载公钥
        rsa_key = RSA.import_key(self.public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        # 加密明文
        ciphertext = cipher.encrypt(plaintext)
        return encode16(ciphertext)  # 十六进制编码

    def decrypt(self, ciphertext):
        # 加载私钥
        rsa_key = RSA.import_key(self.private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        # 解码 Base64 并解密
        ciphertext = decode16(ciphertext)
        decrypted_text = cipher.decrypt(ciphertext)
        return decrypted_text


# 示例
if __name__ == "__main__":
    def generate_rsa_keypair(bits=2048):
        # 生成 RSA 密钥对
        key = RSA.generate(bits)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    # 生成 RSA 密钥对
    private_key, public_key = generate_rsa_keypair()
    print(f'private_key: {private_key.decode()} , \npublic_key: {public_key.decode()}')
    # 要加密的明文
    plaintext = b'This is a secret message.'
    # RSA加解密实例
    address_rsa_client = RSAClient(private_key, public_key)
    # 加密
    ciphertext = address_rsa_client.encrypt(plaintext)
    print("Ciphertext:", ciphertext)
    # 解密x
    decrypted_text = address_rsa_client.decrypt(ciphertext)
    print("Decrypted Text:", decrypted_text)
