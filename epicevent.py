import click
import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from epicevents.controllers.commands import cli_epic
from epicevents.controllers.commands.cli_employee import cli_employee
from epicevents.controllers.commands.cli_client import cli_client
from epicevents.controllers.commands.cli_contract import cli_contract
from epicevents.controllers.commands.cli_event import cli_event


def sentry_activate():
    dsn = "https://8d035592443a8c8d8bcef25a1b7fe5df@o4505946318635008"
    dsn += ".ingest.sentry.io/4505946331086848"
    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            SqlalchemyIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


@click.group(help="------ CRM EpicEvent ------")
def main():
    pass


main.add_command(cli_epic.login)
main.add_command(cli_epic.logout)
main.add_command(cli_epic.dashboard)
main.add_command(cli_epic.initbase)
main.add_command(cli_employee)
main.add_command(cli_client)
main.add_command(cli_contract)
main.add_command(cli_event)


if __name__ == '__main__':
    sentry_activate()
    main()
