# LyteAssignment test framework setup
- Clone the repo and cd to LyteAssignment
- Install python 3.8 or newer
- setup Virtual env
```
python3 -m venv venv
source venv/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```
- Set PYTHONPATH
```
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
- Run the test
```
python3 -m pytest -vs tests/  --html=report.html --self-contained-html --json-report --json-report-file report.json
```
