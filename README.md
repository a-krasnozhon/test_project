# test_project
### Local Development
#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms));
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/)).

#### Configuring Local Environment
Build container
```bash
$ docker-compose -f local.yml build
```

Run application
```bash
$ docker-compose -f local.yml up
```

Run application detached console
```bash
$ docker-compose -f local.yml up -d
```

#### Pytest
```bash
$  docker-compose -f local.yml run --rm app pytest
```

#### Linters

Flake8
```bash
$ docker-compose -f local.yml run --rm app flake8 --statistics --show-source
```

Pylint
```bash
$ docker-compose -f local.yml run --rm app pylint app
```
