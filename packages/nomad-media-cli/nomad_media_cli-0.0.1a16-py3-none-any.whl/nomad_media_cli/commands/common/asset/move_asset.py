import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to move.")
@click.option("--destination-folder-id", required=True, help="The destination folder ID of the move.")
@click.option("--name", required=False, help="The name of the asset when moved.")
@click.option("--batch-action", required=False, help="The batch action of the move in JSON dict format.")
@click.option("--content-definition-id", required=False, help="The content definition ID of the move.")
@click.option("--schema-name", required=False, help="The schema name of the move.")
@click.option("--resolver-exempt", required=False, type=click.BOOL, help="The resolver exempt of the move.")
@click.pass_context
def move_asset(ctx, id, destination_folder_id, name, batch_action, content_definition_id, schema_name, resolver_exempt):
    """Move asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.move_asset(
            id,
            destination_folder_id,
            name,
            json.loads(batch_action) if batch_action else None,
            content_definition_id,
            schema_name,
            resolver_exempt
        )
        click.echo("Asset moved successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error moving asset: {e}"})
        sys.exit(1)