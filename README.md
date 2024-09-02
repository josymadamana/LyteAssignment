# LyteAssignment test framework setup

- Install python 3.8 or newer
- Setup Virtual env
```
python3 -m venv venv
source venv/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```
To run the test
```
python3 -m pytest -vs tests/   --html=report.html --self-contained-html --json-report --json-report-file report.json
```
