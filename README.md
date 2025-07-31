
# TCC - PROF AI

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FastAPI)

## Autores

- [@savinoo](https://github.com/savinoo)
- [@Maycon-M](https://www.github.com/Maycon-M)

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

### PostgreSQL

`PG_SERVER`

`PG_DATABASE`

`PG_UID`

`PG_PWD`

## Documentação da API

A API é auto-documentada em formato de Swagger.

Acesse-a pelo path:

`/docs`

## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/Maycon-M/prof_ai.git
```

Entre no diretório do projeto

```bash
  cd prof_ai
```

Crie uma imagem de docker

```bash
  docker build -t api_prof_ai -f docker/Dockerfile .
```

Instancie um Docker Container

```bash
  docker run -d -p 8888:8888 --env-file .env --name api_prof_ai_container api_prof_ai
```
