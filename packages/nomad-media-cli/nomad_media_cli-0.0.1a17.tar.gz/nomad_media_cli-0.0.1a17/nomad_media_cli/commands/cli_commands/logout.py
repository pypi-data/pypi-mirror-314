from nomad_media_cli.helpers.utils import get_config

import click
import json
import sys

@click.command()
@click.pass_context
def login(ctx):
    """Login to the service"""

    nomad_sdk = ctx.obj["nomad_sdk"]
    get_config(ctx)

    config = ctx.obj["config"]
    config_path = ctx.obj["config_path"]

    try:
        del config["token"]
        del config["refresh_token_val"]
        del config["expiration_seconds"]
        del config["id"]
        
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
            
        #nomad_sdk.logout()
            
    except Exception as e:
        click.echo({ "error": f"Error logging out: {e}" })
        sys.exit(1)