# Restful-api
This project tests the restful api by checking the status code
## Getting Started
### Python Version (Recommend)
    Python 3.8.3

### Install pytest
##### Run the following command in your command line:
    $ pip install -U pytest
##### Check that you installed the correct version:
    $ pytest --version
    This is pytest version 5.4.3, imported from c:\users\user\pycharmprojects\restful-api\venv\lib\site-packages\pytest\__init__.py

### Running the pytest
##### Run the following command in your command line in ../src path for testing all files:
    $ pytest -v
##### Run the following command in your command line in ../src path for tessting a particular files (e.g. unit_test.py):
    $ pytest -v unit_test.py
    
### Install pytest-xdist
#### It allows running tests in parallel with pytest
##### Run the following command in your command line:
    $ pip install pytest-xdist
##### Check that you installed the correct version:
    $ pytest --version
    This is pytest version 5.4.3, imported from c:\users\user\pycharmprojects\restful-api\venv\lib\site-packages\pytest\__init__.py
    setuptools registered plugins:
      pytest-forked-1.3.0 at c:\users\user\pycharmprojects\restful-api\venv\lib\site-packages\pytest_forked\__init__.py
      pytest-xdist-1.34.0 at c:\users\user\pycharmprojects\restful-api\venv\lib\site-packages\xdist\plugin.py
      pytest-xdist-1.34.0 at c:\users\user\pycharmprojects\restful-api\venv\lib\site-packages\xdist\looponfail.py
    
### Running the pytest with pytest-xdist
##### Run the following command in your command line in ../src path with 2 parallel:
    $ pytest -n=2 -v

