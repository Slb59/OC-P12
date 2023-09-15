# import os
# import dotenv
from configparser import ConfigParser


class FileEnvNotExists(Exception):
    def __init__(
            self,
            message="The file database.ini doesn't exists"
            ):
        self.message = message
        super().__init__(self.message)


class NoSectionPostgresql(Exception):
    def __init__(
            self,
            filename,
            section,
            message="The file doesn't have the correct section"
            ):
        self.message = message
        self.section = section
        self.filename = filename
        super().__init__(self.message)

    def __str__(self) -> str:
        return "the file " + self.filename + "doesn't have "\
            + self.section + "section"


class Config():

    def __init__(self, filename='database.ini') -> None:
        self.filename = filename
        section = 'postgresql'
        parser = ConfigParser()
        parser.read(self.filename)
        self.db_config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.db_config[param[0]] = param[1]
        else:
            raise NoSectionPostgresql(section)

    def __str__(self) -> str:
        return str(self.db_config)


# class Environ():

#     def __init__(self) -> None:
#         """
#         Load the .env file
#         :raise FileEnvNotExists if the file doesn't exists
#         or DATABASE var is not set
#         """
#         dotenv_file = dotenv.find_dotenv()
#         dotenv.load_dotenv(dotenv_file)
#         self.DATABASE = os.getenv('DATABASE')
#         if self.DATABASE is None:
#             raise FileEnvNotExists()

#         self.HOST = os.getenv('HOST')
#         self.USER = os.getenv('USER')
#         self.PASSWORD = os.getenv('PASSWORD')
#         self.PORT = os.getenv('PORT')
