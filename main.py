import argparse
from epicevents.controllers.epicmanager import EpicManager


def create_argparser():
    parser = argparse.ArgumentParser(
        prog="EpicEvent",
        description="Gestionnaire d'évènements",
        epilog="------ CRM EpicEvent ------"
    )

    parser.add_argument(
        "--login", type=str,
        help="login username/password"
    )

    parser.add_argument(
        "--logout", action="store_true",
        help="logout"
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = create_argparser()
    app = EpicManager(args)
    app.run()
