import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the screenshot details for.")
@click.option("--segment-id", required=True, help="The ID of the segment.")
@click.option("--screenshot-id", required=True, help="The ID of the screenshot.")
@click.pass_context
def get_asset_screenshot_details(ctx, id, segment_id, screenshot_id):
    """Get asset screenshot details"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_screenshot_details(id, segment_id, screenshot_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset screenshot details: {e}"})
        sys.exit(1)