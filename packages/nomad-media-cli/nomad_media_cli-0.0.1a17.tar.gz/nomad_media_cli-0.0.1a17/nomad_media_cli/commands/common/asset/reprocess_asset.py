import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--target-ids", required=True, help="The target IDs of the reprocess in JSON list format.")
@click.pass_context
def reprocess_asset(ctx, target_ids):
    """Reprocess asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.reprocess_asset(json.loads(target_ids))
        click.echo("Asset reprocessed successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error reprocessing asset: {e}"})
        sys.exit(1)