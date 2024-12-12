
def encode16(secret):
    return secret.hex()

def decode16(secret_16):
    return bytes.fromhex(secret_16)
