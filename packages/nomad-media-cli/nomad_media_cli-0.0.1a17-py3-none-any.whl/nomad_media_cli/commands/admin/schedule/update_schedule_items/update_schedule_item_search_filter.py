import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--schedule-id", required=True, help="The ID of the schedule the schedule item search filter is to be updated from.")
@click.option("--item-id", required=True, help="The ID of the item to be updated.")
@click.option("--collections", required=False, help="The collections of the schedule item search filter in JSON list format.")
@click.option("--days", required=False, help="The days of the schedule item search filter in JSON list format.")
@click.option("--duration-time-code", required=False, help="The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.")
@click.option("--end-search-date", required=False, help="The end search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.")
@click.option("--end-search-duration-in-minutes", required=False, type=click.INT, help="The end search duration in minutes of the schedule item search filter.")
@click.option("--end-time-code", required=False, help="The end time code of the schedule item search filter. Format: hh:mm:ss;ff.")
@click.option("--related-contents", required=False, help="The related contents of the schedule item search filter in JSON list format.")
@click.option("--search-date", required=False, help="The search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.")
@click.option("--search-duration-in-minutes", required=False, type=click.INT, help="The search duration in minutes of the schedule item search filter.")
@click.option("--search-filter-type", required=False, type=click.INT, help="The search filter type of the schedule item search filter. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4")
@click.option("--tags", required=False, help="The tags of the schedule item search filter in JSON list format.")
@click.option("--time-code", required=False, help="The time code of the schedule item search filter. Format: hh:mm:ss;ff.")
@click.pass_context
def update_schedule_item_search_filter(ctx, schedule_id, item_id, collections, days, duration_time_code, end_search_date, end_search_duration_in_minutes, end_time_code, related_contents, search_date, search_duration_in_minutes, search_filter_type, tags, time_code):
    """Update schedule item search filter"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_schedule_item_search_filter(
            schedule_id,
            item_id,
            json.loads(collections) if collections else None,
            json.loads(days) if days else None,
            duration_time_code,
            end_search_date,
            end_search_duration_in_minutes,
            end_time_code,
            json.loads(related_contents) if related_contents else None,
            search_date,
            search_duration_in_minutes,
            search_filter_type,
            json.loads(tags) if tags else None,
            time_code
        )
        click.echo("Schedule item search filter updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating schedule item search filter: {e}"})
        sys.exit(1)