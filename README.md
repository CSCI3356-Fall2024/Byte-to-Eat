# Byte-to-Eat

## setup
use python 3.10.12

### make virtual environment, this way we all are running the same versions of libraries in case there are any conflicsts
python -m venv .venv OR python3 -m venv .venv

### activate venv
WINDOWS: source .venv/bin/activate
MAC: .venv/bin/activate (I think)

### install dependencies
pip install -r requirements.txt

### when adding/removing a new python library please add to requirements.txt then run:
pip -freeze requirements.txt

