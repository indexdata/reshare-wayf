# ReShare WAYF
A simple flask app to resolve appropriate reshare tenants for a request. The Application presents a WAYF form, and then redirects the user to the appropriate ReShare tenant based on the user's selection. If the "Remember me" option is checked, it will set a cookie to remember the selection in order to skip the WAYF next time.

## Setup
Setup python
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set available options in the target_hosts.json file
```
vi config/target_hosts.json
```
## Run (for development)
```
flask --app wayf run
```

## Build and run Docker container
Build:
```
docker build -t reshare-wayf:latest .
```
Run:
```
docker -d run -p 8000:8000
```
