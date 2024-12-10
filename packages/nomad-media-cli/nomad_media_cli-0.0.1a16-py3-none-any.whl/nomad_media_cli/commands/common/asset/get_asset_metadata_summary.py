import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the metadata summary for.")
@click.pass_context
def get_asset_metadata_summary(ctx, id):
    """Get asset metadata summary"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_metadata_summary(id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset metadata summary: {e}"})
        sys.exit(1)