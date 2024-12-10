import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--tag-type", required=True, type=click.Choice(["tag", "collection"]), help="Whether to add a tag or collection to the content.")
@click.option("--id", required=True, help="The ID of the content.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to add the tag/collection for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to add the tag/collection for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--content-definition", required=True, help="The content definition.")
@click.option("--tag-name", required=True, help="The name of the tag or collection.")
@click.option("--tag-id", required=False, help="The ID of the tag or collection.")
@click.option("--create-new", required=True, type=click.BOOL, help="The create new flag.")
@click.pass_context
def add_tag_or_collection(ctx, tag_type, id, url, object_key, content_definition, tag_name, tag_id, create_new):
    """Add tag or collection to content"""
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
        result = nomad_sdk.add_tag_or_collection(
            tag_type,
            id,
            content_definition,
            tag_name,
            tag_id,
            create_new
        )
        click.echo("Tag or collection added successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error adding tag or collection: {e}"})
        sys.exit(1)