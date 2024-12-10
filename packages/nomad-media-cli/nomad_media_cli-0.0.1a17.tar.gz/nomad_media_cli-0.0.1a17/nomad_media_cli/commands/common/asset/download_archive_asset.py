import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--ids", help="The IDs of the assets to be downloaded in JSON list format.")
@click.option("--urls", help="The Nomad URL(s) of the Asset(s) (file or folder) to download the archive(s) for (bucket::object-key).")
@click.option("--object-keys", help="Object-key(s) only of the Asset(s) (file or folder) to download the archive(s) for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--file-name", required=False, help="The file name of the archive asset.")
@click.option("--download-proxy", required=False, type=click.BOOL, help="The download proxy of the archive asset.")
@click.pass_context
def download_archive_asset(ctx, ids, urls, object_keys, file_name, download_proxy):
    """Download archive asset"""
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
        result = nomad_sdk.download_archive_asset(
            ids,
            file_name,
            download_proxy
        )
        click.echo("Archive asset downloaded successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error downloading archive asset: {e}"})
        sys.exit(1)