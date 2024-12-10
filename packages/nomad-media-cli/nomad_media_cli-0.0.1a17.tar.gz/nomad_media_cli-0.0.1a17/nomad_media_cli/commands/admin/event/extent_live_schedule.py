import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--event-id", required=True, help="The ID of the event to extend the live schedule of.")
@click.option("--recurring-days", required=True, help="The days of the week to extend the live schedule of in JSON list format.")
@click.option("--recurring-weeks", required=True, type=click.INT, help="The number of weeks to extend the live schedule of.")
@click.option("--end-date", required=False, help="The end date to extend the live schedule of.")
@click.pass_context
def extend_live_schedule(ctx, event_id, recurring_days, recurring_weeks, end_date):
    """Extend live schedule of event"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.extend_live_schedule(
            event_id,
            json.loads(recurring_days),
            recurring_weeks,
            end_date
        )
        click.echo("Live schedule extended successfully.")

    except Exception as e:
        click.echo({"error": f"Error extending live schedule: {e}"})
        sys.exit(1)