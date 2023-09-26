from sqlalchemy.engine import URL
from sqlalchemy_utils.functions import (
    database_exists,
    create_database, drop_database,
)
from epicevents.controllers.config import Config

if __name__ == '__main__':
    db = Config()
    print(db)
    url = URL.create(
            drivername="postgresql",
            database=db.db_config['database'],
            host=db.db_config['host'],
            username=db.db_config['user'],
            password=db.db_config['password'],
            port=int(db.db_config['port'])
        )
    print(url)
    if database_exists(url):
        print('Erreur : La base de données existe déjà')
    else:
        print('creation...')
