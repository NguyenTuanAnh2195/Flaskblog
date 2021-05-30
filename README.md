1. Install Pyenv, use Python3.7.5:
```
https://github.com/pyenv/pyenv
```

2. Create database `blog_db` and user `someuser`, view `config.py` for more details
3. Create virtual environment:
```
python -m venv env
```
4. Install required dependencies:
```
pip install -r requirements.txt
```
5. Create .env file
```
FLASK_APP = app
FLASK_ENV = development
```
6. Run and test app
```
flask run
```
7. Run linter test with tox (Unit tests not yet available)
```
tox
```