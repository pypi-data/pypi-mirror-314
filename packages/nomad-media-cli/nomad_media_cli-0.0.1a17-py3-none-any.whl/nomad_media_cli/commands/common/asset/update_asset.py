import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to update.")
@click.option("--display-name", required=False, help="The display name of the asset.")
@click.option("--display-date", required=False, help="The display date of the asset.")
@click.option("--available-start-date", required=False, help="The available start date of the asset.")
@click.option("--available-end-date", required=False, help="The available end date of the asset.")
@click.option("--custom-properties", required=False, help="The custom properties of the asset in JSON dict format.")
@click.pass_context
def update_asset(ctx, id, display_name, display_date, available_start_date, available_end_date, custom_properties):
    """Update asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.update_asset(
            id,
            display_name,
            display_date,
            available_start_date,
            available_end_date,
            json.loads(custom_properties) if custom_properties else None
        )
        click.echo("Asset updated successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error updating asset: {e}"})
        sys.exit(1)