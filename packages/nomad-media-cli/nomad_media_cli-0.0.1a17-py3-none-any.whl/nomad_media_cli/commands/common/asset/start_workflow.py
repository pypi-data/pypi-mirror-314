import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--action-arguments", required=True, help="The action arguments of the start in JSON dict format.")
@click.option("--target-ids", required=True, help="The target IDs of the start in JSON list format.")
@click.pass_context
def start_workflow(ctx, action_arguments, target_ids):
    """Start workflow"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.start_workflow(json.loads(action_arguments), json.loads(target_ids))
        click.echo("Workflow started successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error starting workflow: {e}"})
        sys.exit(1)