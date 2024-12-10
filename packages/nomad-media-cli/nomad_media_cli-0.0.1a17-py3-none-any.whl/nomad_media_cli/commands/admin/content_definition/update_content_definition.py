import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--content-definition-id", required=True, help="The ID of the content definition to update.")
@click.option("--name", required=False, help="The name of the content definition.")
@click.option("--content-fields", required=False, help="The content fields of the content definition in JSON list format.")
@click.option("--content-definition-group", required=False, help="The content definition group of the content definition.")
@click.option("--content-definition-type", required=False, help="The content definition type of the content definition.")
@click.option("--display-field", required=False, help="The display field of the content definition.")
@click.option("--route-item-name-field", required=False, help="The name of the route item.")
@click.option("--security-groups", required=False, multiple=True, help="The security group(s) of the content definition. Multiple flags for multiple security groups.")
@click.option("--system-roles", required=False, multiple=True, help="The system roles of the content definition. Multiple flags for multiple system roles.")
@click.option("--include-in-tags", required=False, type=click.BOOL, help="Whether to include the content definition in tags.")
@click.option("--index-content", required=False, type=click.BOOL, help="Whether to index the content.")
@click.pass_context
def update_content_definition(ctx, content_definition_id, name, content_fields, content_definition_group, content_definition_type, display_field, route_item_name_field, security_groups, system_roles, include_in_tags, index_content):
    """Update content definition by id"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        content_fields_list = json.loads(content_fields) if content_fields else None

        nomad_sdk.update_content_definition(
            content_definition_id, name, content_fields_list, content_definition_group, content_definition_type,
            display_field, route_item_name_field, security_groups, system_roles, include_in_tags, index_content
        )
        click.echo("Content definition updated successfully.")

    except Exception as e:
        click.echo({"error": f"Error updating content definition: {e}"})
        sys.exit(1)