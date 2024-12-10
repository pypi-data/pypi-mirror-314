import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to update the ad break for.")
@click.option("--ad-break-id", required=True, help="The ID of the ad break.")
@click.option("--time-code", required=False, help="The time code of the asset ad break. Format: hh:mm:ss;ff.")
@click.option("--tags", required=False, help="The tags of the asset ad break in JSON list format.")
@click.option("--labels", required=False, help="The labels of the asset ad break in JSON list format.")
@click.pass_context
def update_asset_ad_break(ctx, id, ad_break_id, time_code, tags, labels):
    """Update asset ad break"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_asset_ad_break(
            id,
            ad_break_id,
            time_code,
            json.loads(tags) if tags else None,
            json.loads(labels) if labels else None
        )
        click.echo("Asset ad break updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating asset ad break: {e}"})
        sys.exit(1)