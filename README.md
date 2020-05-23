# Assistt Rest API

To start, clone assist-restapi-backend repo
```
git clone https://github.com/tuum-tech/assist-restapi-backend.git;
cd assist-restapi-backend;
```

# Prerequisites
- Python3 is needed
```
brew install python3 // On Mac
sudo apt-get install python3 // On linux
```
- Virtualenv
```
pip3 install virtualenv
```

# Setup
- Create a python virtual environment
```
virtualenv -p `which python3` venv
```
- Activate the virtualenv environment
```
source venv/bin/activate
```
- Install the dependencies
```
pip install -r requirements.txt
```
- Run mongodb
```
cd tools
./mongodb.sh
```

# Run
- Start API server
```
waitress-serve --port=8000 restapi:api // On Windows
gunicorn restapi:api --bind='0.0.0.0:8000' // On mac/linux
```

# Verify
- To create a transaction, run the following:
```
curl http://localhost:8000/create?didid=didexemple&payload=test
```
- To verify the transaction, run the following:
```
curl http://localhost:8000/verify?transactionid=9f760fcd-9523-4899-9f58-44efdb2d3c7s
```