import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--live-channel-id", required=True, help="The ID of the live channel to clip.")
@click.option("--start-time-code", required=False, help="The start time code of the live channel to clip.")
@click.option("--end-time-code", required=False, help="The end time code of the live channel to clip.")
@click.option("--title", required=False, help="The title of the live channel to clip.")
@click.option("--output-folder-id", required=True, help="The output folder ID of the live channel to clip.")
@click.option("--tags", required=False, help="The tags of the live channel to clip in JSON list format.")
@click.option("--collections", required=False, help="The collections of the live channel to clip in JSON list format.")
@click.option("--related-contents", required=False, help="The related contents of the live channel to clip in JSON list format.")
@click.option("--video-bitrate", required=False, type=click.INT, help="The video bitrate of the live channel to clip.")
@click.option("--audio-tracks", required=False, help="The audio tracks of the live channel to clip in JSON list format.")
@click.pass_context
def clip_live_channel(ctx, live_channel_id, start_time_code, end_time_code, title, output_folder_id, tags, collections, related_contents, video_bitrate, audio_tracks):
    """Clip live channel"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.clip_live_channel(
            live_channel_id,
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
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error clipping live channel: {e}"})
        sys.exit(1)