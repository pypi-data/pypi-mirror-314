import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the asset ad breaks for.")
@click.pass_context
def get_asset_ad_breaks(ctx, id):
    """Get asset ad breaks"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_ad_breaks(id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset ad breaks: {e}"})
        sys.exit(1)