import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the segment details for.")
@click.option("--segment-id", required=True, help="The ID of the segment.")
@click.pass_context
def get_asset_segment_details(ctx, id, segment_id):
    """Get asset segment details"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_segment_details(id, segment_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset segment details: {e}"})
        sys.exit(1)