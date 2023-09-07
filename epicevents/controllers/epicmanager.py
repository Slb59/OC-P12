import os
from dotenv import load_dotenv


class EpicManager:

    def __init__(self):
        ...

    def __str__(self):
        return "CRM EPIC EVENTS"

    def run(self):

        # load .env file
        load_dotenv()
        print(os.getenv('DATABASE'))

        # create database
        # init database structure
        # init data
        # login

        # show menu
        running = True

        while running:
            running = False
