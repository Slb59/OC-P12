import os
import dotenv
from configparser import ConfigParser


def create_config(basename, username, password, port):
    data = [
        '[postgresql]',
        f'DATABASE = {basename}',
        'HOST = localhost',
        f'USER = {username}',
        f'PASSWORD = {password}',
        f'PORT = {port}'
    ]
    
    file = open("database.ini", "w")
    for line in data:
        file.write(line + "\n")
    file.close()


class FileNotExists(Exception):
    def __init__(
            self,
            filename,
            message="The file doesn't exists"
            ):
        self.message = message
        self.filename = filename
        super().__init__(self.message)

    def __str__(self) -> str:
        return "the file " + self.filename + " doesn't exists"


class NoSectionPostgresql(Exception):
    def __init__(
            self,
            filename,
            section='',
            message="The file doesn't have the correct section"
            ):
        self.message = message
        self.section = section
        self.filename = filename
        super().__init__(self.message)

    def __str__(self) -> str:
        return "the file " + self.filename + " doesn't have "\
            + self.section + " section"


class Config():

    def __init__(self, filename='database.ini') -> None:
        self.filename = filename
        section = 'postgresql'
        parser = ConfigParser()

        try:
            with open(self.filename):
                parser.read(self.filename)
        except IOError:
            raise FileNotExists(self.filename)

        self.db_config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.db_config[param[0]] = param[1]
        else:
            raise NoSectionPostgresql(filename='database.ini', section=section)

    def __str__(self) -> str:
        return str(self.db_config)


class Environ():

    def __init__(self) -> None:
        """
        Load the .env file
        :raise FileEnvNotExists if the file doesn't exists
        """
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        self.DEFAULT_DATABASE = os.getenv('DEFAULT_DATABASE')
        if self.DEFAULT_DATABASE is None:
            raise FileNotExists(dotenv_file)

        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.TOKEN_DELTA = int(os.getenv('TOKEN_DELTA'))
