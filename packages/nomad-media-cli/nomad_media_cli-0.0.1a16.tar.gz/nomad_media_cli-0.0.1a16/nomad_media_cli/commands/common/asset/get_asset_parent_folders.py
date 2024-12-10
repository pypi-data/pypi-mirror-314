import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The asset ID of the current item to get the parents for.")
@click.option("--page-size", required=True, type=click.INT, help="The size of the page of folders to retrieve.")
@click.pass_context
def get_asset_parent_folders(ctx, id, page_size):
    """Get asset parent folders"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_parent_folders(id, page_size)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset parent folders: {e}"})
        sys.exit(1)