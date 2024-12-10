import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--live-operator-id", required=True, help="The ID of the live operator.")
@click.option("--preroll-asset-id", required=False, help="The preroll asset ID of the live operator.")
@click.option("--postroll-asset-id", required=False, help="The postroll asset ID of the live operator.")
@click.option("--live-input-id", required=False, help="The live input ID of the live operator.")
@click.option("--related-content-ids", required=False, help="The related content IDs of the live operator in JSON list format.")
@click.option("--tag-ids", required=False, help="The tag IDs of the live operator in JSON list format.")
@click.pass_context
def start_broadcast(ctx, live_operator_id, preroll_asset_id, postroll_asset_id, live_input_id, related_content_ids, tag_ids):
    """Start broadcast"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.start_broadcast(
            live_operator_id,
            preroll_asset_id,
            postroll_asset_id,
            live_input_id,
            json.loads(related_content_ids) if related_content_ids else None,
            json.loads(tag_ids) if tag_ids else None
        )
        click.echo("Broadcast started successfully.")

    except Exception as e:
        click.echo({"error": f"Error starting broadcast: {e}"})
        sys.exit(1)