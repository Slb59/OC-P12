import argparse
import click
import sentry_sdk
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


@click.command
def hello():
    click.echo('Hello')


if __name__ == '__main__':
    dsn = "https://8d035592443a8c8d8bcef25a1b7fe5df@o4505946318635008"
    dsn += ".ingest.sentry.io/4505946331086848"
    sentry_sdk.init(
        dsn=dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
    args = create_argparser()
    app = EpicManager(args)
    app.run()
