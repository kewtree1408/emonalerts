#EMonAlerts is easy monitoring for your servers.

## Run via docker:
```
docker build . -t emonalerts
docker run -d -v $PWD/success.toml:/app/success.toml -v $PWD/credentials.json:/app/credentials.json emonalerts
```

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

## Example of credentials from email:
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
./src/runner.py success.toml credentials.json -v -a
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
