import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to create the annotation for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to create the annotation for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--start-time-code", required=True, help="The start time code of the annotation. Format: hh:mm:ss;ff.")
@click.option("--end-time-code", required=False, help="The end time code of the annotation. Format: hh:mm:ss;ff.")
@click.option("--title", required=False, help="The title of the annotation.")
@click.option("--summary", required=False, help="The summary of the annotation.")
@click.option("--description", required=False, help="The description of the annotation.")
@click.pass_context
def create_annotation(ctx, id, url, object_key, start_time_code, end_time_code, title, summary, description):
    """Create annotation"""
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
        result = nomad_sdk.create_annotation(
            id,
            start_time_code,
            end_time_code,
            title,
            summary,
            description
        )
        click.echo("Annotation created successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error creating annotation: {e}"})
        sys.exit(1)