import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--parent-id", required=True, help="The parent asset ID for the placeholder asset.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to create the placeholder asset for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to create the placeholder asset for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--asset-name", required=True, help="The visual name of the new placeholder. It can contain spaces and other characters, must contain file extension.")
@click.pass_context
def create_placeholder_asset(ctx, parent_id, url, object_key, asset_name):
    """Create placeholder asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if url or object_key:
        if url and "::" not in url:
            click.echo({ "error": "Please provide a valid path or set the default bucket." })               
            sys.exit(1)
        if object_key:
            if "bucket" in ctx.obj:
                url = f"{ctx.obj['bucket']}::{object_key}"
            else:
                click.echo({ "error": "Please set bucket using `set-bucket` or use url." })
                sys.exit(1)
                
        url_search_results = nomad_sdk.search(None, None, None, [{
            "fieldName": "url",
            "operator": "equals",
            "values": url
        }], None, None, None, None, None, None, None, None, None)
        
        if not url_search_results or len(url_search_results["items"] == 0):
            click.echo({ "error": f"URL {url} not found." })
            sys.exit(1)
            
        parent_id = url_search_results["items"][0]["id"]

    try:
        result = nomad_sdk.create_placeholder_asset(parent_id, asset_name)
        click.echo("Placeholder asset created successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating placeholder asset: {e}"})
        sys.exit(1)