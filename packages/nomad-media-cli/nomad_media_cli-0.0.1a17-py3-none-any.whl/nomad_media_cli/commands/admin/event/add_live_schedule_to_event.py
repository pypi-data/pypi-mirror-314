import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--event-id", required=True, help="The ID of the event to add the live schedule to.")
@click.option("--slate-video", required=False, help="The slate video ID of the event in JSON dict format.")
@click.option("--preroll-video", required=False, help="The preroll video of the event in JSON dict format.")
@click.option("--postroll-video", required=False, help="The postroll video of the event in JSON dict format.")
@click.option("--is-secure-output", required=False, type=click.BOOL, help="Whether the event is secure output.")
@click.option("--archive-folder", required=False, help="The archive folder of the event in JSON dict format.")
@click.option("--primary-live-input", required=False, help="The live input A ID of the event in JSON dict format.")
@click.option("--backup-live-input", required=False, help="The live input B ID of the event in JSON dict format.")
@click.option("--primary-livestream-input-url", required=False, help="The primary live stream URL of the event.")
@click.option("--backup-livestream-input-url", required=False, help="The backup live stream URL of the event.")
@click.option("--external-output-profiles", required=False, help="The external output profiles of the event in JSON list format.")
@click.option("--status", required=False, help="Current status of the Live Channel Settings configuration in JSON dict format.")
@click.option("--status-message", required=False, help="The status message of the event.")
@click.option("--live-channel", required=False, help="The live channel of the event in JSON dict format.")
@click.option("--override-settings", required=False, type=click.BOOL, help="Whether to override the settings of the event.")
@click.option("--output-profile-group", required=False, help="The output profile group of the event in JSON dict format.")
@click.pass_context
def add_live_schedule_to_event(ctx, event_id, slate_video, preroll_video, postroll_video, is_secure_output, archive_folder, primary_live_input, backup_live_input, primary_livestream_input_url, backup_livestream_input_url, external_output_profiles, status, status_message, live_channel, override_settings, output_profile_group):
    """Add live schedule to event"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.add_live_schedule_to_event(
            event_id,
            json.loads(slate_video) if slate_video else None,
            json.loads(preroll_video) if preroll_video else None,
            json.loads(postroll_video) if postroll_video else None,
            is_secure_output,
            json.loads(archive_folder) if archive_folder else None,
            json.loads(primary_live_input) if primary_live_input else None,
            json.loads(backup_live_input) if backup_live_input else None,
            primary_livestream_input_url,
            backup_livestream_input_url,
            json.loads(external_output_profiles) if external_output_profiles else None,
            json.loads(status) if status else None,
            status_message,
            json.loads(live_channel) if live_channel else None,
            override_settings,
            json.loads(output_profile_group) if output_profile_group else None
        )
        click.echo("Live schedule added to event successfully.")

    except Exception as e:
        click.echo({"error": f"Error adding live schedule to event: {e}"})
        sys.exit(1)