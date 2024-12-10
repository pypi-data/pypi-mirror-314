import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to transcribe.")
@click.option("--transcript-id", required=True, help="The ID of the transcript.")
@click.option("--transcript", required=False, help="The transcript of the transcribe in JSON list format.")
@click.pass_context
def transcribe_asset(ctx, id, transcript_id, transcript):
    """Transcribe asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.transcribe_asset(
            id,
            transcript_id,
            json.loads(transcript) if transcript else None
        )
        click.echo("Asset transcribed successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error transcribing asset: {e}"})
        sys.exit(1)