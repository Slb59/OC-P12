# import psycopg2

# conn = psycopg2.connect(database="db_name",
#                         host="db_host",
#                         user="db_user",
#                         password="db_pass",
#                         port="db_port")

from sqlalchemy import create_engine
from sqlalchemy.engine import URL


url = URL.create(
    drivername="postgresql",
    database="epic",
    host="db_host",
    username="db_user",
    password="db_pass",
    port="db_port"
)

engine = create_engine(url)
conn = engine.connect()