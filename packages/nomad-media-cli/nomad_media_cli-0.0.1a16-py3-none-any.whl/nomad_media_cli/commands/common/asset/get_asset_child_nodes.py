import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to get the asset child nodes for.")
@click.option("--folder-id", required=True, help="The ID of the folder the asset is in.")
@click.option("--sort-column", required=True, help="The column to sort by.")
@click.option("--is-desc", required=True, type=click.BOOL, help="Whether the sort is descending or not.")
@click.option("--page-index", required=True, type=click.INT, help="The page index of the asset child nodes.")
@click.option("--page-size", required=True, type=click.INT, help="The page size of the asset child nodes.")
@click.pass_context
def get_asset_child_nodes(ctx, id, folder_id, sort_column, is_desc, page_index, page_size):
    """Get asset child nodes"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset_child_nodes(id, folder_id, sort_column, is_desc, page_index, page_size)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting asset child nodes: {e}"})
        sys.exit(1)