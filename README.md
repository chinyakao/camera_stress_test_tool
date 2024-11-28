# Camera Stress Test Tool
Running camera stress test by webcamtests.com

## Pre-request
1. Ubuntu OS with installed git/pyhon3/python3-venv
  ```
  sudo apt update
  sudo apt install git python3 python3-pip python3-venv
  ```
2. Windows OS with installed git/python3/virtualenv

## Setup
```
git clone https://github.com/chinyakao/camera_stress_test_tool.git
cd camera_stress_test_tool
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
```
source .venv/bin/activate
python3 run_stress_test.py -c {running cycles}
```

leave venv
```
deactivate
```

catch the log under the `/log` folder
