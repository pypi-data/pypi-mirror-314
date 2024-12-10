import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--schedule-id", required=True, help="The ID of the schedule the live channel item is to be added to.")
@click.option("--days", required=True, help="The days of the schedule item live channel in JSON list format.")
@click.option("--duration-time-code", required=True, help="The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.")
@click.option("--end-time-code", required=True, help="The end time code of the schedule item live channel. Format: hh:mm:ss;ff.")
@click.option("--live-channel", required=True, help="The live channel of the schedule item live channel in JSON dict format.")
@click.option("--previous-item", required=False, help="The previous item of the schedule item live channel.")
@click.option("--time-code", required=True, help="The time code of the schedule item live channel. Format: hh:mm:ss;ff.")
@click.pass_context
def create_schedule_item_live_channel(ctx, schedule_id, days, duration_time_code, end_time_code, live_channel, previous_item, time_code):
    """Create schedule item live channel"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_schedule_item_live_channel(
            schedule_id,
            json.loads(days),
            duration_time_code,
            end_time_code,
            json.loads(live_channel),
            previous_item,
            time_code
        )
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating schedule item live channel: {e}"})
        sys.exit(1)