import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--sources", required=True, help="The sources of the media in JSON list format.")
@click.option("--title", required=False, help="The title of the media.")
@click.option("--tags", required=False, help="The tags of the media in JSON list format.")
@click.option("--collections", required=False, help="The collections of the media in JSON list format.")
@click.option("--related-contents", required=False, help="The related contents of the media in JSON list format.")
@click.option("--destination-folder-id", required=True, help="The destination folder ID of the media.")
@click.option("--video-bitrate", required=False, type=click.INT, help="The video bitrate of the media.")
@click.option("--audio-tracks", required=False, help="The audio tracks of the media in JSON list format.")
@click.pass_context
def build_media(ctx, sources, title, tags, collections, related_contents, destination_folder_id, video_bitrate, audio_tracks):
    """Build media"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.build_media(
            json.loads(sources),
            title,
            json.loads(tags) if tags else None,
            json.loads(collections) if collections else None,
            json.loads(related_contents) if related_contents else None,
            destination_folder_id,
            video_bitrate,
            json.loads(audio_tracks) if audio_tracks else None
        )
        click.echo("Media built successfully.")

    except Exception as e:
        click.echo({"error": f"Error building media: {e}"})
        sys.exit(1)