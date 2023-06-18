**Activate the virtual environment**
-

```commandline
source blockchain-env/bin/activate
```

**Install all packages**
-
```commandline
pip install -r requirements.txt
```

**Run code via cmd / PATH is the structure to the file / py_file being the python file without extension**
-
```commandline
python3 -m PATH.py_flie 
```

**Run Pytest when testing the methods/functions of the blockchain / where PATH is the path to the directory**
-
Ensure the virtual environment is running first before running these test (step 1)
```commandline
python3 -m pytest PATH
python3 -m pytest backend/test
```

**Run the application and API**
-
Ensure the virtual environment is running first before running these test (step 1)
```commandline
python3 -m backend.App
```