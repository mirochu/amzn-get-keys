import re
import base64
def get_pssh(pssh_long: str = None):
    PATTERN=r"000000[1-9][1-9]707373"
    try: long_hex = base64.b64decode(pssh_long).hex()
    except: return None
    match = re.search(PATTERN, long_hex)
    if match:
        print("Found PSSH header!")
        pssh_hex = long_hex[match.start():]
        pssh = base64.b64encode(bytes.fromhex(pssh_hex)).decode()
        return pssh
    else:
        return None