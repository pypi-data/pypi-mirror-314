import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from key_sdk.utils import encode16, decode16


class AESClient(object):
    def __init__(
            self,
            keys: dict,
            latest_key_version: str,
            default_iv: bytes = None,
    ):
        """
        aes密钥列表，key为密钥版本，value为密钥
        keys = {
            "default": b"\x95\xce\xce\xc6\x05=\x14~R@\xdc\xca\xccNU4\xad|\xdf&Z\xb4\xf2|\xd2'7\x06a\x8e\xa3\xe1",
            "jf-12-xxxxxxxx": b'\x0b\x9d\xa1\xcb\xc1\xca\xa3\x9f\x99\x12\x11\x08A5\xcb\x01\xf4\xbd\x0f\xb7sb\xb4\x86`\xc5\xb85N+\xc0\xec',
        }
        """
        # 密钥详情
        self.keys = keys
        # 当前最新的密钥版本
        self.latest_key_version = latest_key_version
        # 默认IV，只有解密旧密文时使用
        self.default_iv = default_iv

    @property
    def latest_key(self):
        # 最新的key
        return self.get_key_by_version(self.latest_key_version)

    def get_key_by_version(self, version):
        if isinstance(version, bytes):
            version = version.decode()
        # 根据密钥版本获取key
        key = self.keys.get(version)
        if not key:
            raise Exception(f'lose key, version: {version}')
        return key

    def encrypt(self, plaintext):
        """加密默认使用最新的版本的密钥和随机iv，都拼接到密文里"""
        # 生成随机的 IV（16 字节）
        iv = os.urandom(16)
        # 最新的密钥
        key = self.latest_key
        # 创建 AES CBC 模式的加密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 使用 PKCS7 填充明文
        padded_plaintext = pad(plaintext, AES.block_size)
        # 加密明文
        ciphertext = cipher.encrypt(padded_plaintext)
        # 返回 IV 和密文的组合，并进行 十六进制 编码
        ciphertext = encode16(iv + ciphertext)
        # 添加密钥版本头
        return f'{self.latest_key_version}#{ciphertext}'

    def decrypt(self, ciphertext):
        """自动兼容老密文解密，新的密文以密钥版本开头"""
        if ciphertext.startswith('jf-'):
            return self.decrypt_new_ciphertext(ciphertext)
        else:
            return self.decrypt_default_ciphertext(ciphertext)

    def decrypt_default_ciphertext(self, ciphertext):
        iv = self.default_iv
        key = self.keys.get('default')
        return self.decrypt_ciphertext(key, iv, ciphertext)

    def decrypt_new_ciphertext(self, ciphertext):
        # 获取密钥版本
        key_version, ciphertext = ciphertext.split('#')
        # 解码 十六进制 编码的密文
        ciphertext_with_iv = decode16(ciphertext)
        # 提取 IV 和密文
        iv = ciphertext_with_iv[:16]
        ciphertext = ciphertext_with_iv[16:]
        key = self.get_key_by_version(version=key_version)
        return self.decrypt_ciphertext(key, iv, ciphertext)

    @staticmethod
    def decrypt_ciphertext(key, iv, ciphertext):
        # 创建 AES CBC 模式的解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 解密并去除填充
        decrypted_padded = cipher.decrypt(ciphertext)
        return unpad(decrypted_padded, AES.block_size)  # 去除填充并返回解密结果

# 示例
if __name__ == "__main__":
    # AES-256 需要 32 字节的密钥
    key = os.urandom(32)  # 生成一个随机的 32 字节密钥
    # 要加密的明文
    plaintext = b'\x80\xbd\x81=\xb9\xcf(\xc0eI\xe8\x1de\xf4\xc2\x1b\\|gVh\xe73\xa4\r\x97\xb2\xe1f\x90(\x88'
    # AES加解密实例
    keys = {
        "default": b"\x95\xce\xce\xc6\x05=\x14~R@\xdc\xca\xccNU4\xad|\xdf&Z\xb4\xf2|\xd2'7\x06a\x8e\xa3\xe1",
        "jf-12-xxxxxxxx": b'\x0b\x9d\xa1\xcb\xc1\xca\xa3\x9f\x99\x12\x11\x08A5\xcb\x01\xf4\xbd\x0f\xb7sb\xb4\x86`\xc5\xb85N+\xc0\xec',
    }
    phone_aes_client = AESClient(keys, latest_key_version='jf-12-xxxxxxxx', default_iv=None)
    # 加密
    ciphertext = phone_aes_client.encrypt(plaintext)
    print("Ciphertext :", ciphertext)
    # 解密
    decrypted_text = phone_aes_client.decrypt(ciphertext)
    print("Decrypted Text:", decrypted_text)
