import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--live-operator-id", required=True, help="The ID of the live operator.")
@click.option("--related-content-ids", required=False, help="The related content IDs of the live operator in JSON list format.")
@click.option("--tag-ids", required=False, help="The tag IDs of the live operator in JSON list format.")
@click.pass_context
def complete_segment(ctx, live_operator_id, related_content_ids, tag_ids):
    """Complete segment"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.complete_segment(
            live_operator_id,
            json.loads(related_content_ids) if related_content_ids else None,
            json.loads(tag_ids) if tag_ids else None
        )
        click.echo("Segment completed successfully.")

    except Exception as e:
        click.echo({"error": f"Error completing segment: {e}"})
        sys.exit(1)