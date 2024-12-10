import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--name", required=True, help="The name of the live output profile.")
@click.option("--output-type", required=False, help="The type of the live output profile in JSON dict format.")
@click.option("--enabled", required=False, type=click.BOOL, help="Indicates if the live output profile is enabled.")
@click.option("--audio-bitrate", required=False, type=click.INT, help="The audio bitrate of the live output profile.")
@click.option("--output-stream-key", required=False, help="The output stream key of the live output profile.")
@click.option("--output-url", required=False, help="The output URL of the live output profile.")
@click.option("--secondary-output-stream-key", required=False, help="The secondary output stream key of the live output profile.")
@click.option("--secondary-url", required=False, help="The secondary URL of the live output profile.")
@click.option("--video-bitrate", required=False, type=click.INT, help="The video bitrate of the live output profile.")
@click.option("--video-bitrate-mode", required=False, help="The video bitrate mode of the live output profile. The modes are CBR and VBR.")
@click.option("--video-codec", required=False, help="The video codec of the live output profile. The codecs are H264 and H265.")
@click.option("--video-frames-per-second", required=False, type=click.INT, help="The video frames per second of the live output profile.")
@click.option("--video-height", required=False, type=click.INT, help="The video height of the live output profile.")
@click.option("--video-width", required=False, type=click.INT, help="The video width of the live output profile.")
@click.pass_context
def create_live_output_profile(ctx, name, output_type, enabled, audio_bitrate, output_stream_key, output_url, secondary_output_stream_key, secondary_url, video_bitrate, video_bitrate_mode, video_codec, video_frames_per_second, video_height, video_width):
    """Create live output profile"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_live_output_profile(
            name,
            json.loads(output_type) if output_type else None,
            enabled,
            audio_bitrate,
            output_stream_key,
            output_url,
            secondary_output_stream_key,
            secondary_url,
            video_bitrate,
            video_bitrate_mode,
            video_codec,
            video_frames_per_second,
            video_height,
            video_width
        )
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating live output profile: {e}"})
        sys.exit(1)