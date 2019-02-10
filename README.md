# EMonAlerts is easy monitoring for your servers.

[![Build Status](https://travis-ci.com/kewtree1408/emonalerts.svg?token=sN2juxZGRBsY3B6bKghG&branch=master)](https://travis-ci.com/kewtree1408/emonalerts)

## Example of config:
```toml
# This is a TOML document.

title = "TOML Example for EasyMonAlerts"

[owner]
name = "Victoria Fantasy"
emails = [
    "me@vika.space",
    "vi@umc8.ru"
]

[period]
minutes = 5

# Urls for ping

[servers]

    [servers.friendly_name4]
    host = "google.com"
    schemes = ["https"]
    ports = [ 443 ]

    [servers.friendly_name5]
    host = "vika.space"
    schemes = ["https"]
    ports = [ 443 ]

```

## Example of email credentials:
If you have an email from which are you going to send the information about services:
```json
{
    "email": "easy.mon.alerts@gmail.com",
    "password": "******",
    "host": "smtp.gmail.com",
    "port": "465"
}
```

## How to run:
```bash
cd emonalerts/
python3 -m venv .venv
source edocmon/.venv/bin/activate
pip install -r src/req.txt
./src/runner.py success.toml -v -a
./src/runner.py success.toml -e credentials.json -v -a
```

## How to run tests:
```
cd edocmon/
tox
```

How to run one test:
```
tox -- src/tests/test_utils.py::TestHostSettings::test_host_settings
```

## Run via docker:
Check:
```
docker build . -t emonalerts
```

```
touch checker.db
docker run -d \
    -v $PWD/problems.toml:/app/example.toml \
    -v $PWD/credentials.json:/app/credentials.json \
    -v $PWD/checker.db:/app/emonalerts/db/checker.db \
    emonalerts /app/runner.py /app/example.toml -e /app/credentials.json -a -v
```

```
docker run -d \
    -v $PWD/success.toml:/app/example.toml \
    -v $PWD/checker.db:/app/emonalerts/db/checker.db \
    emonalerts /app/runner.py /app/example.toml -a -v
```
