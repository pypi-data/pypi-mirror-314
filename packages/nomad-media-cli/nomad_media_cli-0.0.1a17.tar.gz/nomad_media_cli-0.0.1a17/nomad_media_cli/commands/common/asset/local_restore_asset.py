import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to local restore.")
@click.option("--profile", required=False, help="The profile of the local restore.")
@click.pass_context
def local_restore_asset(ctx, id, profile):
    """Local restore asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.local_restore_asset(id, profile)
        click.echo("Asset local restored successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error local restoring asset: {e}"})
        sys.exit(1)