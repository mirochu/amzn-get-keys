#Script to get SD keys with L3 cdm from Amazon Prime - Greetings to TPD94 and rlaphoenix!

from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests
import base64
import os
import curl
from helpers.get_pssh import get_pssh

def get_wvd():
    wvd_files = 0
    for file in os.listdir(f"{os.getcwd()}/device"):
        if file.endswith(".wvd"):
            wvd_files += 1
    if wvd_files > 1:
        for file in os.listdir(f"{os.getcwd()}/device"):
            if file.endswith(".wvd"):
                print(file)       
        while True:
            choice = input(f"Please select wvd: ")
            if ".wvd" in choice:
                if os.path.isfile(f"{os.getcwd()}/device/{choice}"):
                    return (f"{os.getcwd()}/device/{choice}")
            print("Invalid choice!")
    elif wvd_files == 1:
        return(f"{os.getcwd()}/device/{os.listdir(f"{os.getcwd()}/device")[0]}")
    raise Exception("No .wvd file found!")

def get_amzn_keys(user_pssh: str = None, lic_url: str = None):
    pssh = PSSH(user_pssh)
    device = Device.load(get_wvd())
    cdm = Cdm.from_device(device)
    session_id = cdm.open()
    challenge = cdm.get_license_challenge(session_id, pssh)
    widevine2challenge = base64.b64encode(challenge).decode() 
    lic = requests.post(url=lic_url, headers=curl.headers, cookies=curl.cookies, params=curl.params, data={"widevine2Challenge": widevine2challenge, "includeHdcpTestKeyInLicense": "true"}) 
    lic.raise_for_status()
    try: 
        cdm.parse_license(session_id, lic.json()["widevine2License"]["license"])
    except Exception as e:
            if "'untrusted_device'" in str(lic.json()):
                raise Exception("Untrusted CDM")
            else:
                print ("BEGIN OF JSON")
                print (lic.json())
                print("END OF JSON")
                raise e
    if cdm.get_keys(session_id) is not None:    
        keys = []
        for key in cdm.get_keys(session_id):
            if key.type == "CONTENT":
                keys.append(f" {key.kid.hex}:{key.key.hex()}")
        print("Got keys!")
        return(keys)
    else:
        raise Exception("Could not find keys!")

if __name__ == "__main__":
    regions = ["https://atv-ps-eu.primevideo.com/cdp/catalog/GetPlaybackResources", "https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources"]
    print("Select region:\n\t1. EUR\n\t2. USA")
    region = int(input("Choice: ")) - 1
    license_url = regions[region]
    pssh_long = input("PSSH: ")
    pssh = get_pssh(pssh_long)
    if pssh is None:
        print("Invalid PSSH")
        exit(1)
    keys = get_amzn_keys(pssh, license_url)
    for key in keys:
        print (key)