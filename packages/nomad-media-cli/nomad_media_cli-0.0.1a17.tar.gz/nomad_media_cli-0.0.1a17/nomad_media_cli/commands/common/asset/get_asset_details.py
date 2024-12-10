import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the details for.")
@click.pass_context
def get_asset_details(ctx, id):
    """Get asset details"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_details(id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset details: {e}"})
        sys.exit(1)