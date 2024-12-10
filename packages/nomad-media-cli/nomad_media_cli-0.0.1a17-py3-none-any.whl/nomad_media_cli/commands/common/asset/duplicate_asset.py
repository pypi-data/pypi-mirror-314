import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to be duplicated.")
@click.pass_context
def duplicate_asset(ctx, id):
    """Duplicate asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.duplicate_asset(id)
        click.echo("Asset duplicated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error duplicating asset: {e}"})
        sys.exit(1)