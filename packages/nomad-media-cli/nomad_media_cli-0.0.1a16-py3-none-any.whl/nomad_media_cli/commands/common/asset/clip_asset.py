import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to be clipped.")
@click.option("--start-time-code", required=True, help="The start time code of the asset. Format: hh:mm:ss;ff.")
@click.option("--end-time-code", required=True, help="The end time code of the asset. Format: hh:mm:ss;ff.")
@click.option("--title", required=True, help="The title of the asset.")
@click.option("--output-folder-id", required=True, help="The output folder ID of the asset.")
@click.option("--tags", required=False, help="The tags of the asset in JSON list format.")
@click.option("--collections", required=False, help="The collections of the asset in JSON list format.")
@click.option("--related-contents", required=False, help="The related contents of the asset in JSON list format.")
@click.option("--video-bitrate", required=False, type=click.INT, help="The video bitrate of the asset.")
@click.option("--audio-tracks", required=False, help="The audio tracks of the asset in JSON list format.")
@click.pass_context
def clip_asset(ctx, id, start_time_code, end_time_code, title, output_folder_id, tags, collections, related_contents, video_bitrate, audio_tracks):
    """Clip asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.clip_asset(
            id,
            start_time_code,
            end_time_code,
            title,
            output_folder_id,
            json.loads(tags) if tags else None,
            json.loads(collections) if collections else None,
            json.loads(related_contents) if related_contents else None,
            video_bitrate,
            json.loads(audio_tracks) if audio_tracks else None
        )
        click.echo("Asset clipped successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error clipping asset: {e}"})
        sys.exit(1)