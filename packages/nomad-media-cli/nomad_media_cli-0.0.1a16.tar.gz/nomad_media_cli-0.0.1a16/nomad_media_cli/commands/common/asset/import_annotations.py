import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to import the annotations for.")
@click.option("--annotations", required=True, help="The annotations to import in JSON list format.")
@click.pass_context
def import_annotations(ctx, id, annotations):
    """Import annotations"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.import_annotations(id, json.loads(annotations))
        click.echo("Annotations imported successfully.")

    except Exception as e:
        click.echo({"error": f"Error importing annotations: {e}"})
        sys.exit(1)