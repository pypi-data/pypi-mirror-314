import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to update the language for.")
@click.option("--language-id", required=True, help="The ID of the language.")
@click.pass_context
def update_asset_language(ctx, id, language_id):
    """Update asset language"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_asset_language(id, language_id)
        click.echo("Asset language updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating asset language: {e}"})
        sys.exit(1)