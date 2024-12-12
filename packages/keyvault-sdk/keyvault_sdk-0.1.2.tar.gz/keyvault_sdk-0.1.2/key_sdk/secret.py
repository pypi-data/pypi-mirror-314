import requests
import base64


class KeyRequest(object):
    def __init__(
            self,
            host: str,
            app_name: str,
            app_secret: str,
            aes_key_sid: str = None,
            rsa_private_key_sid: str = None,
            login_url: str = '/api/vault/app/login',
            ase_key_version_url: str = '/api/vault/secret/version',
            ase_key_url: str = '/api/vault/secret/aes',
            rsa_key_url: str = '/api/vault/secret/rsa',
            **kwargs
    ):
        # 服务地址
        self.host = host
        # 登陆url
        self.login_url = login_url
        # 会话保持
        self.token = None
        # 应用名
        self.app_name = app_name
        # 应用secret
        self.app_secret = app_secret
        # aes
        # aes密钥版本列表接口
        self.ase_key_version_url = ase_key_version_url
        # aes密钥获取接口
        self.ase_key_url = ase_key_url
        # ase密钥sid
        self.aes_key_sid = aes_key_sid
        # rsa
        # rsa私钥获取接口
        self.rsa_key_url = rsa_key_url
        # rsa私钥sid
        self.rsa_private_key_sid = rsa_private_key_sid
        # app login
        self.login()

    def base_post(self, url, payload, headers=None):
        response = requests.post(url=url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f'req error, code: {response.status_code}, url: {url}, text: {response.text}')
        result = response.json()
        code = result['code']
        if code == 200:
            return result['data']
        elif code == 401:
            self.login()  # token失效，重新获取
        else:
            raise Exception(f'req error, code: {code}, url: {url}, result: {result}')

    def post(self, url, payload):
        headers = {'token': self.token}
        return self.base_post(url, payload, headers)

    def login(self):
        payload = {'app_name': self.app_name, 'app_secret': self.app_secret}
        url = f'{self.host}{self.login_url}'
        result = self.base_post(url=url, payload=payload)
        self.token = result['token']

    def get_aes_key_version(self):
        payload = {'app_name': self.app_name, 'sid': self.aes_key_sid}
        url = f'{self.host}{self.ase_key_version_url}'
        result = self.post(url, payload)
        return result['versions']

    def get_aes_key(self, version):
        payload = {'app_name': self.app_name, 'sid': self.aes_key_sid, 'version': version}
        url = f'{self.host}{self.ase_key_url}'
        result = self.post(url, payload)
        key = result['key']
        return self.xor_decrypt(key, self.token)

    def get_rsa_key(self):
        payload = {'app_name': self.app_name, 'sid': self.rsa_private_key_sid}
        url = f'{self.host}{self.rsa_key_url}'
        result = self.post(url, payload)
        private_key = result['plaintext']
        return self.xor_decrypt(private_key, self.token)

    @staticmethod
    def xor_decrypt(content, key):
        if not isinstance(content, bytes):
            content = content.encode()
        if not isinstance(key, bytes):
            key = key.encode()
        content = base64.b64decode(content, validate=True)
        # xor解密
        encrypted_data = bytearray()
        for i in range(len(content)):
            encrypted_data.append(content[i] ^ key[i % len(key)])
        return bytes(encrypted_data)


if __name__ == '__main__':
    # 测试示例
    kwargs = {
        'host': 'http://127.0.0.1:9094',
        'app_name': 'test',
        'app_secret': '1111111111111',
        'aes_key_sid': 'sid-xxxxxxxxxxxxxxx',
        'rsa_private_key_sid': 'sid-yyyyyyyyyyyyy',
    }
    key_handler = KeyRequest(**kwargs)
    versions = key_handler.get_aes_key_version()
    version = versions[-1] if versions else None
    aes_key = key_handler.get_aes_key(version)
    print(f'aes key: {aes_key}')
    rsa_private_key = key_handler.get_rsa_key()
    print(f'rsa private key: {rsa_private_key.decode()}')
