import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--schedule-id", required=True, help="The ID of the schedule the playlist is to be updated from.")
@click.option("--default-video-asset", required=False, help="The default video asset of the playlist in JSON dict format.")
@click.option("--loop-playlist", required=False, type=click.BOOL, help="Whether or not to loop the playlist.")
@click.option("--name", required=False, help="The name of the playlist.")
@click.option("--thumbnail-asset", required=False, help="The thumbnail asset of the playlist in JSON dict format.")
@click.pass_context
def update_playlist(ctx, schedule_id, default_video_asset, loop_playlist, name, thumbnail_asset):
    """Update playlist"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_playlist(
            schedule_id,
            json.loads(default_video_asset) if default_video_asset else None,
            loop_playlist,
            name,
            json.loads(thumbnail_asset) if thumbnail_asset else None
        )
        click.echo("Playlist updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating playlist: {e}"})
        sys.exit(1)