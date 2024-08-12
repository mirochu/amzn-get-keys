# AMZN-GET-KEYS
Simple pywidevine wrapper of pywidevine for amazon(dot)com (VOD) and primevideo(dot)com (SD@L3)
## Usage

 1. Install requirements.txt
	 

    pip install -r requirements.txt

 2. Create .wvd file with pywidevine:
 

    pywidevine create-device -t ANDROID -l 3 -c path/to/client_id.bin -k path/to/private_key.pem

 3.  Put .wvd in device folder
 4. Paste license headers and cookies in curl.py
 5.  Run amzn.py

## Features

 - Region selector (Hard coded and ugly)
 - PSSH header finder


