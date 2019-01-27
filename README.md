EMonAlerts is easy monitoring for your servers.

[test badge]
[version python badge]
[docker hub]

Test example:
1. Docker pull regisrety...
2. Docker run my image

How to create a config:

example.toml
- email
- hostnames list
- ping interval

How to run

docker run ...

How to use:
```
source edocmon/.venv/bin/activate
./src/runner.py success.toml credentials.json -v -a
```

How to run tests:
```
cd edocmon/
tox
```

How to run one test:
```
tox -- src/tests/test_utils.py::TestHostSettings::test_host_settings
```
