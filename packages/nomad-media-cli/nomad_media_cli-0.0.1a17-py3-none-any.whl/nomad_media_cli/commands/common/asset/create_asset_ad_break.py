import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to create the asset ad break for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to create the asset ad break for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--time-code", required=False, help="The time code of the asset ad break. Format: hh:mm:ss;ff.")
@click.option("--tags", required=False, help="The tags of the asset ad break in JSON list format.")
@click.option("--labels", required=False, help="The labels of the asset ad break in JSON list format.")
@click.pass_context
def create_asset_ad_break(ctx, id, url, object_key, time_code, tags, labels):
    """Create asset ad break"""
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
            
        id = url_search_results["items"][0]["id"]

    try:
        result = nomad_sdk.create_asset_ad_break(
            id,
            time_code,
            json.loads(tags) if tags else None,
            json.loads(labels) if labels else None
        )
        click.echo("Asset ad break created successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating asset ad break: {e}"})
        sys.exit(1)