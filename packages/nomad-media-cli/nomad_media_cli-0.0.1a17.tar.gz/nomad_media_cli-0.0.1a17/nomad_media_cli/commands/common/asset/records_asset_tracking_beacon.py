import click
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to record the asset tracking beacon for.")
@click.option("--tracking-event", required=True, help="The tracking event of the asset tracking beacon.")
@click.option("--live-channel-id", required=True, help="The live channel ID of the asset tracking beacon.")
@click.option("--content-id", required=False, help="Optional content ID to track along with required asset ID.")
@click.option("--second", required=True, type=click.INT, help="Second mark into the video/ad.")
@click.pass_context
def records_asset_tracking_beacon(ctx, id, tracking_event, live_channel_id, content_id, second):
    """Record asset tracking beacon"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.records_asset_tracking_beacon(id, tracking_event, live_channel_id, content_id, second)
        click.echo("Asset tracking beacon recorded successfully.")

    except Exception as e:
        click.echo({"error": f"Error recording asset tracking beacon: {e}"})
        sys.exit(1)