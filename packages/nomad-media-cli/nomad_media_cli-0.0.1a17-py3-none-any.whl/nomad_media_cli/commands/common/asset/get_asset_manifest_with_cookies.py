import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the manifest with cookies for.")
@click.option("--cookie-id", required=True, help="The ID of the cookie.")
@click.pass_context
def get_asset_manifest_with_cookies(ctx, id, cookie_id):
    """Get asset manifest with cookies"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_manifest_with_cookies(id, cookie_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset manifest with cookies: {e}"})
        sys.exit(1)