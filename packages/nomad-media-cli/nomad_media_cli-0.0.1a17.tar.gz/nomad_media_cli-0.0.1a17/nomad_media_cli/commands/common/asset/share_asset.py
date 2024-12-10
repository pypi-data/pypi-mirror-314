import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to share.")
@click.option("--nomad-users", required=False, help="The nomad users of the share in JSON list format.")
@click.option("--external-users", required=False, help="The external users of the share in JSON list format.")
@click.option("--shared-duration-in-hours", required=False, type=click.INT, help="The share duration in hours of the share.")
@click.pass_context
def share_asset(ctx, id, nomad_users, external_users, shared_duration_in_hours):
    """Share asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.share_asset(
            id,
            json.loads(nomad_users) if nomad_users else None,
            json.loads(external_users) if external_users else None,
            shared_duration_in_hours
        )
        click.echo("Asset shared successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error sharing asset: {e}"})
        sys.exit(1)