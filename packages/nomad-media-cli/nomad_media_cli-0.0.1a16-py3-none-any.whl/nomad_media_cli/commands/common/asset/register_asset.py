import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=False, help="The ID of the asset to register.")
@click.option("--parent-id", required=False, help="The ID of the parent.")
@click.option("--display-object-key", required=False, help="The display object key of the register.")
@click.option("--bucket-name", required=True, help="The bucket name of the register.")
@click.option("--object-key", required=True, help="The object key of the register.")
@click.option("--e-tag", required=False, help="The eTag of the register.")
@click.option("--tag-ids", required=False, help="The tags of the register in JSON list format.")
@click.option("--collection-ids", required=False, help="The collections of the register in JSON list format.")
@click.option("--related-content-ids", required=False, help="The related contents of the register in JSON list format.")
@click.option("--sequencer", required=False, help="The sequencer of the register.")
@click.option("--asset-status", required=False, help="The asset status of the register.")
@click.option("--storage-class", required=False, help="The storage class of the register.")
@click.option("--asset-type", required=False, help="The asset type of the register.")
@click.option("--content-length", required=False, type=click.INT, help="The content length of the register.")
@click.option("--storage-event-name", required=False, help="The storage event name of the register.")
@click.option("--created-date", required=False, help="The created date of the register.")
@click.option("--storage-source-ip-address", required=False, help="The storage source IP address of the register.")
@click.option("--start-media-processor", required=False, type=click.BOOL, help="The start media processor of the register.")
@click.option("--delete-missing-asset", required=False, type=click.BOOL, help="The delete missing asset of the register.")
@click.pass_context
def register_asset(ctx, id, parent_id, display_object_key, bucket_name, object_key, e_tag, tag_ids, collection_ids, related_content_ids, sequencer, asset_status, storage_class, asset_type, content_length, storage_event_name, created_date, storage_source_ip_address, start_media_processor, delete_missing_asset):
    """Register asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.register_asset(
            id,
            parent_id,
            display_object_key,
            bucket_name,
            object_key,
            e_tag,
            json.loads(tag_ids) if tag_ids else None,
            json.loads(collection_ids) if collection_ids else None,
            json.loads(related_content_ids) if related_content_ids else None,
            sequencer,
            asset_status,
            storage_class,
            asset_type,
            content_length,
            storage_event_name,
            created_date,
            storage_source_ip_address,
            start_media_processor,
            delete_missing_asset
        )
        click.echo("Asset registered successfully.")
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error registering asset: {e}"})
        sys.exit(1)