import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to update the annotation for.")
@click.option("--annotation-id", required=True, help="The ID of the annotation.")
@click.option("--start-time-code", required=True, help="The start time code of the annotation. Format: hh:mm:ss;ff.")
@click.option("--end-time-code", required=True, help="The end time code of the annotation. Format: hh:mm:ss;ff.")
@click.option("--title", required=False, help="The title of the annotation.")
@click.option("--summary", required=False, help="The summary of the annotation.")
@click.option("--description", required=False, help="The description of the annotation.")
@click.pass_context
def update_annotation(ctx, id, annotation_id, start_time_code, end_time_code, title, summary, description):
    """Update annotation"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_annotation(
            id,
            annotation_id,
            start_time_code,
            end_time_code,
            title,
            summary,
            description
        )
        click.echo("Annotation updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating annotation: {e}"})
        sys.exit(1)