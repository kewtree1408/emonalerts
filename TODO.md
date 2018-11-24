1. Add docker secrets -
2. Add docker file +
3. Add docker volume for toml, logs and amount of errors +
4. Add easy docker installation +
5. Add tests
6. Add linter
7. Fix all linters errors
8. Add CI/CD for linter/tests/docker update
9. Add uptime on SQLlite: calculate successful and unsuccessful data and store in one line in MySQL



docker build . -t emonalerts
docker run -d -v $PWD/default.toml:/app/default.toml -v $PWD/credentials.json:/app/credentials.json -v $PWD/checker.db:/app/checker.db emonalerts