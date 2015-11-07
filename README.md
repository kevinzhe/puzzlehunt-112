# puzzlehunt-112-f15
### Dev server setup
1. Get virtualenv for Python 3 (from pip: `pip3 install virtualenv`, or get it from your package manager)
2. Create a virtualenv directory in the root folder: `virtualenv venv` (or `virtualenv3 venv`)
3. Source the virtualenv setup script: `source venv/bin/activate`
4. Install the requirements: `pip install -r requirements.txt`
5. Run the db migrations: `python puzzlehunt_112_f15/manage.py migrate`
6. Run the dev server: `python puzzlehunt_112_f15/manage.py runserver`
