1. Add docker secrets
2. Add docker file
3. Add docker volume for toml, logs and amount of errors
4. Add easy docker installation
5. Add tests
6. Add linter
7. Fix all linters errors
8. Add CI/CD for linter/tests/docer update


docker run -d --name easymonalerts -v volume-config:/config nginx:latest

docker run -d -v $PWD/default.toml:/app/default.toml -v $PWD/credentials.json:/app/credentials.json emonalerts