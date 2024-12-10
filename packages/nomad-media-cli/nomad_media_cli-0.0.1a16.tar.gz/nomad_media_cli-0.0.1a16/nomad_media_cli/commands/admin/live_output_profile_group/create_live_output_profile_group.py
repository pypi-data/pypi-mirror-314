import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--name", required=True, help="The name of the live output profile group.")
@click.option("--is-enabled", required=True, type=click.BOOL, help="Indicates if the live output profile group is enabled.")
@click.option("--manifest-type", required=True, help="The manifest type of the live output profile group. The types are HLS, DASH, and BOTH.")
@click.option("--is-default-group", required=True, type=click.BOOL, help="Indicates if the live output profile group is the default group.")
@click.option("--live-output-type", required=True, help="The type of the live output profile group in JSON list format.")
@click.option("--archive-live-output-profile", required=False, help="The archive live output profile of the live output profile group in JSON list format.")
@click.option("--live-output-profiles", required=True, help="The live output profiles of the live output profile group in JSON list format.")
@click.pass_context
def create_live_output_profile_group(ctx, name, is_enabled, manifest_type, is_default_group, live_output_type, archive_live_output_profile, live_output_profiles):
    """Create live output profile group"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_live_output_profile_group(
            name,
            is_enabled,
            manifest_type,
            is_default_group,
            json.loads(live_output_type),
            json.loads(archive_live_output_profile) if archive_live_output_profile else None,
            json.loads(live_output_profiles)
        )
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating live output profile group: {e}"})
        sys.exit(1)