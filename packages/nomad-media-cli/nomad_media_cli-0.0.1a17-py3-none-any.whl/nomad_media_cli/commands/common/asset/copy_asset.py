import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--ids", required=False, multiple=True, help="The ID(s) of the assets to be copied")
@click.option("--urls", required=False, multiple=True, help="The Nomad URL(s) of the Asset (file or folder) to copy the assets for (bucket::object-key).")
@click.option("--object-keys", required=False, multiple=True, help="Object-key(s) only of the Asset (file or folder) to copy the assets for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--destination-folder-id", required=True, help="The destination folder ID of the assets.")
@click.option("--batch-action", required=False, help="The actions to be performed in JSON dict format.")
@click.option("--content-definition-id", required=False, help="The content definition ID of the assets.")
@click.option("--schema-name", required=False, help="The schema name of the assets.")
@click.option("--resolver-exempt", required=False, type=click.BOOL, help="The resolver exempt of the assets.")
@click.pass_context
def copy_asset(ctx, ids, urls, object_keys, destination_folder_id, batch_action, content_definition_id, schema_name, resolver_exempt):
    """Copy asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    for url in urls:
        if url and "::" not in url:
            click.echo({ "error": "Please provide a valid path or set the default bucket." })               
            sys.exit(1)
        
        url_search_results = nomad_sdk.search(None, None, None, [{
            "fieldName": "url",
            "operator": "equals",
            "values": url
        }], None, None, None, None, None, None, None, None, None)
        
        if not url_search_results or len(url_search_results["items"] == 0):
            click.echo({ "error": f"URL {url} not found." })
            sys.exit(1)
            
        ids.append(url_search_results["items"][0]["id"])
        
    for object_key in object_keys:
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
            
        ids.append(url_search_results["items"][0]["id"])

    try:
        result = nomad_sdk.copy_asset(
            ids,
            destination_folder_id,
            json.loads(batch_action) if batch_action else None,
            content_definition_id,
            schema_name,
            resolver_exempt
        )
        click.echo("Asset copied successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error copying asset: {e}"})
        sys.exit(1)