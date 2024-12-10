import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--schedule-id", required=True, help="The ID of the schedule the intelligent playlist is to be updated.")
@click.option("--collections", required=False, help="The collections of the intelligent playlist in JSON list format.")
@click.option("--end-search-date", required=False, help="The end search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.")
@click.option("--end-search-duration-in-minutes", required=False, type=click.INT, help="The end search duration in minutes of the intelligent playlist.")
@click.option("--name", required=False, help="The name of the intelligent playlist.")
@click.option("--related-contents", required=False, help="The related content of the intelligent playlist in JSON list format.")
@click.option("--search-date", required=False, help="The search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.")
@click.option("--search-duration-in-minutes", required=False, type=click.INT, help="The search duration in minutes of the intelligent playlist.")
@click.option("--search-filter-type", required=False, type=click.INT, help="The search filter type of the intelligent playlist. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4")
@click.option("--tags", required=False, help="The tags of the intelligent playlist in JSON list format.")
@click.option("--thumbnail-asset", required=False, help="The thumbnail asset of the intelligent playlist in JSON dict format.")
@click.pass_context
def update_intelligent_playlist(ctx, schedule_id, collections, end_search_date, end_search_duration_in_minutes, name, related_contents, search_date, search_duration_in_minutes, search_filter_type, tags, thumbnail_asset):
    """Update intelligent playlist"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_intelligent_playlist(
            schedule_id,
            json.loads(collections) if collections else None,
            end_search_date,
            end_search_duration_in_minutes,
            name,
            json.loads(related_contents) if related_contents else None,
            search_date,
            search_duration_in_minutes,
            search_filter_type,
            json.loads(tags) if tags else None,
            json.loads(thumbnail_asset) if thumbnail_asset else None
        )
        click.echo("Intelligent playlist updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating intelligent playlist: {e}"})
        sys.exit(1)