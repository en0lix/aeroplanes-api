PS C:\Users\User\PycharmProjects\PythonProject8> pytest --cov=src --cov-report=html --cov-report=xml --cov-report=term
======================================================================================================= test session starts =======================================================================================================
platform win32 -- Python 3.12.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\User\PycharmProjects\PythonProject8
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.2, cov-7.1.0
collected 10 items                                                                                                                                                                                                                 

tests\test_aeroplane.py .....                                                                                                                                                                                                [ 50%]
tests\test_api.py ..                                                                                                                                                                                                         [ 70%]
tests\test_storage.py ...                                                                                                                                                                                                    [100%]

========================================================================================================= tests coverage ==========================================================================================================
_________________________________________________________________________________________ coverage: platform win32, python 3.12.7-final-0 _________________________________________________________________________________________

Name                          Stmts   Miss  Cover
-------------------------------------------------
src\__init__.py                   0      0   100%
src\aeroplanes\__init__.py        0      0   100%
src\aeroplanes\aeroplane.py      65     10    85%
src\aeroplanes\api.py            25      2    92%
src\aeroplanes\main.py           34     34     0%
src\aeroplanes\storage.py        39      0   100%
-------------------------------------------------
TOTAL                           163     46    72%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml
======================================================================================================= 10 passed in 1.21s ========================================================================================================