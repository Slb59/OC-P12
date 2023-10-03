import click
import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from epicevents.controllers.commands import epic_commands
from epicevents.controllers.commands import employee_commands


@click.group(help="------ CRM EpicEvent ------")
def cli():
    pass


cli.add_command(epic_commands.login)
cli.add_command(epic_commands.logout)
cli.add_command(epic_commands.dashboard)

cli.add_command(employee_commands.mydata)
cli.add_command(employee_commands.update_mydata)


if __name__ == '__main__':
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
    cli()
