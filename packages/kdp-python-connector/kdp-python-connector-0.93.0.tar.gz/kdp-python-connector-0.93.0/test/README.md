# Testing KDP Python Connector

## Running tests

### First run setup on the project root to build the python connector
(sudo may be needed)
```
python3 setup.py install
```

### All tests from command line
- from test folder at project root 
```
python -m unittest
```

### Individually

```
python -m unittest -v test_ingest.TestIngest
```

### Single test case

```
python -m unittest -v test_ingest.TestIngest.test_ingest_batch_sizing
```



