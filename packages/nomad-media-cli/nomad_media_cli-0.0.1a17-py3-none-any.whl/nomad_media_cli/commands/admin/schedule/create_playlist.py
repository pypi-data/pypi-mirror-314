import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--name", required=True, help="The name of the playlist.")
@click.option("--thumbnail-asset", required=False, help="The thumbnail asset of the playlist in JSON dict format.")
@click.option("--loop-playlist", required=True, type=click.BOOL, help="Whether the playlist is looped.")
@click.option("--default-video-asset", required=True, help="The default video asset of the playlist in JSON dict format.")
@click.pass_context
def create_playlist(ctx, name, thumbnail_asset, loop_playlist, default_video_asset):
    """Create playlist"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_playlist(
            name,
            json.loads(thumbnail_asset) if thumbnail_asset else None,
            loop_playlist,
            json.loads(default_video_asset)
        )
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating playlist: {e}"})
        sys.exit(1)