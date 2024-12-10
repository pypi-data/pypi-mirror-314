import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--content-id", required=True, help="The ID of the content to update.")
@click.option("--content-definition-id", required=True, help="The ID of the content definition the content belongs to.")
@click.option("--properties", required=True, help="The properties to update in JSON dict format.")
@click.option("--language-id", required=False, help="The language id of the asset to upload.")
@click.pass_context
def update_content(ctx, content_id, content_definition_id, properties, language_id):
    """Update content by id"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        properties_dict = json.loads(properties)
        result = nomad_sdk.update_content(content_id, content_definition_id, properties_dict, language_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating content: {e}"})
        sys.exit(1)