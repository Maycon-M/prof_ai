import os
from urllib.parse import quote_plus

PG_SERVER = os.getenv("PG_SERVER")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_UID = os.getenv("PG_UID")
PG_PWD = os.getenv("PG_PWD")

if PG_PWD is None:
    raise ValueError("PG_PWD não está definido no ambiente")

if isinstance(PG_PWD, bytes):
    encoded_password = quote_plus(PG_PWD)
elif isinstance(PG_PWD, str):
    encoded_password = quote_plus(PG_PWD, encoding="utf-8")
else:
    raise TypeError("PG_PWD não é do tipo esperado")

PG_CONNECTION_STRING = (
    f"postgresql+psycopg2://{PG_UID}:{encoded_password}"
    f"@{PG_SERVER}/{PG_DATABASE}"
)
