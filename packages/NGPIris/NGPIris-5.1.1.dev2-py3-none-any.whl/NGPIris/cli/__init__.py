
import click
from click.core import Context
from json import dump
from pathlib import Path
from botocore.paginate import PageIterator, Paginator
from typing import Any, Generator
from os import get_terminal_size
from math import floor
from tabulate import tabulate
from bitmath import Byte, TiB

from NGPIris.hcp import HCPHandler

def get_HCPHandler(context : Context) -> HCPHandler:
    return context.obj["hcph"]

def format_list(list_of_things : list) -> str:
    list_of_buckets = list(map(lambda s : s + "\n", list_of_things))
    return "".join(list_of_buckets).strip("\n")

def _list_objects_generator(hcph : HCPHandler, name_only : bool) -> Generator[str, Any, None]:
    """
    Handle object list as a paginator that `click` can handle. It works slightly 
    different from `list_objects` in `hcp.py` in order to make the output 
    printable in a terminal
    """
    paginator : Paginator = hcph.s3_client.get_paginator("list_objects_v2")
    pages : PageIterator = paginator.paginate(Bucket = hcph.bucket_name)
    (nb_of_cols, _) = get_terminal_size()
    max_width = floor(nb_of_cols / 5)
    if (not name_only):
        yield tabulate(
            [],
            headers = ["Key", "LastModified", "ETag", "Size", "StorageClass"],
            tablefmt = "plain",
            stralign = "center"
        ) + "\n" + "-"*nb_of_cols + "\n"
    for object in pages.search("Contents[?!ends_with(Key, '/')][]"): # filter objects that does not end with "/"
        if name_only:
            yield str(object["Key"]) + "\n"
        else:
            yield tabulate(
                [
                    [str(object["Key"]), 
                        str(object["LastModified"]), 
                        str(object["ETag"]), 
                        str(object["Size"]), 
                        str(object["StorageClass"])]
                ],
                maxcolwidths = max_width,
                tablefmt = "plain"
            ) + "\n" + "-"*nb_of_cols + "\n"

def object_is_folder(object_path : str, hcph : HCPHandler) -> bool:
    return (object_path[-1] == "/") and (hcph.get_object(object_path)["ContentLength"] == 0)

@click.group()
@click.argument("credentials")
@click.version_option(package_name = "NGPIris")
@click.pass_context
def cli(context : Context, credentials : str):
    """
    NGP Intelligence and Repository Interface Software, IRIS. 
    
    CREDENTIALS refers to the path to the JSON credentials file.
    """
    context.ensure_object(dict)
    context.obj["hcph"] = HCPHandler(credentials)

@cli.command()
@click.argument("bucket")
@click.argument("source")
@click.argument("destination")
@click.pass_context
def upload(context : Context, bucket : str, source : str, destination : str):
    """
    Upload files to an HCP bucket/namespace. 
    
    BUCKET is the name of the upload destination bucket.

    SOURCE is the path to the file or folder of files to be uploaded.
    
    DESTINATION is the destination path on the HCP. 
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    if Path(source).is_dir():
        hcph.upload_folder(source, destination)
    else:
        hcph.upload_file(source, destination)

@cli.command()
@click.argument("bucket")
@click.argument("source")
@click.argument("destination")
@click.option(
    "-f", 
    "--force", 
    help = "Overwrite existing file with the same name (single file download only)", 
    is_flag = True
)
@click.option(
    "-iw", 
    "--ignore_warning", 
    help = "Ignore the download limit", 
    is_flag = True
)
@click.pass_context
def download(context : Context, bucket : str, source : str, destination : str, force : bool, ignore_warning : bool):
    """
    Download a file or folder from an HCP bucket/namespace.

    BUCKET is the name of the download source bucket.

    SOURCE is the path to the object or object folder to be downloaded.

    DESTINATION is the folder where the downloaded object or object folder is to be stored locally. 
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    if not Path(destination).exists():
        Path(destination).mkdir()
    
    if object_is_folder(source, hcph):
        if source == "/":
            source = ""

        cumulative_download_size = Byte(0)
        if not ignore_warning:
            click.echo("Computing download size...")
            for object in hcph.list_objects(source):
                object : dict
                cumulative_download_size += Byte(object["Size"])
                if cumulative_download_size >= TiB(1):
                    click.echo("WARNING: You are about to download more than 1 TB of data. Is this your intention? [y/N]: ", nl = False)
                    inp = click.getchar(True)
                    if inp == "y" or inp == "Y":
                        break
                    else: # inp == "n" or inp == "N" or something else
                        exit("\nAborting download")
    
        hcph.download_folder(source, Path(destination).as_posix())
    else: 
        if Byte(hcph.get_object(source)["ContentLength"]) >= TiB(1):
            click.echo("WARNING: You are about to download more than 1 TB of data. Is this your intention? [y/N]: ", nl = False)
            inp = click.getchar(True)
            if inp == "y" or inp == "Y":
                pass
            else: # inp == "n" or inp == "N" or something else
                exit("\nAborting download")

        downloaded_source = Path(destination) / Path(source).name
        if downloaded_source.exists() and not force:
            exit("Object already exists. If you wish to overwrite the existing file, use the -f, --force option")
        hcph.download_file(source, downloaded_source.as_posix())

@cli.command()
@click.argument("bucket")
@click.argument("object")
@click.pass_context
def delete_object(context : Context, bucket : str, object : str):
    """
    Delete an object from an HCP bucket/namespace. 

    BUCKET is the name of the bucket where the object to be deleted exist.

    OBJECT is the name of the object to be deleted.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.delete_object(object)

@cli.command()
@click.argument("bucket")
@click.argument("folder")
@click.pass_context
def delete_folder(context : Context, bucket : str, folder : str):
    """
    Delete a folder from an HCP bucket/namespace. 

    BUCKET is the name of the bucket where the folder to be deleted exist.

    FOLDER is the name of the folder to be deleted.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.delete_folder(folder)

@cli.command()
@click.pass_context
def list_buckets(context : Context):
    """
    List the available buckets/namespaces on the HCP.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    click.echo(format_list(hcph.list_buckets()))

@cli.command()
@click.argument("bucket")
@click.option(
    "-no", 
    "--name-only", 
    help = "Output only the name of the objects instead of all the associated metadata", 
    default = False
)
@click.pass_context
def list_objects(context : Context, bucket : str, name_only : bool):
    """
    List the objects in a certain bucket/namespace on the HCP.

    BUCKET is the name of the bucket in which to list its objects.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    click.echo_via_pager(_list_objects_generator(hcph, name_only))

@cli.command()
@click.argument("bucket")
@click.argument("search_string")
@click.option(
    "-cs", 
    "--case_sensitive", 
    help = "Use case sensitivity? Default value is False", 
    default = False
)
@click.pass_context
def simple_search(context : Context, bucket : str, search_string : str, case_sensitive : bool):
    """
    Make simple search using substrings in a bucket/namespace on the HCP.

    BUCKET is the name of the bucket in which to make the search.

    SEARCH_STRING is any string that is to be used for the search.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    list_of_results = hcph.search_objects_in_bucket(search_string, case_sensitive)
    click.echo("Search results:")
    for result in list_of_results:
        click.echo("- " + result)

@cli.command()
@click.argument("bucket")
@click.pass_context
def test_connection(context : Context, bucket : str):
    """
    Test the connection to a bucket/namespace.

    BUCKET is the name of the bucket for which a connection test should be made.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    click.echo(hcph.test_connection(bucket))

@click.command()
@click.option(
    "--path",
    help = "Path for where to put the new credentials file.",
    default = ""
)
@click.option(
    "--name",
    help = "Custom name for the credentials file. Will filter out everything after a \".\" character, if any exist.",
    default = "credentials"
)
def iris_generate_credentials_file(path : str, name : str):
    """
    Generate blank credentials file for the HCI and HCP. 

    WARNING: This file will store sensitive information (such as passwords) in plaintext.
    """
    credentials_dict = {
        "hcp" : {
            "endpoint" : "",
            "aws_access_key_id" : "",
            "aws_secret_access_key" : ""
        },
        "hci" : {
            "username" : "",
            "password" : "",
            "address" : "",
            "auth_port" : "",
            "api_port" : ""
        }
    }

    name = name.split(".")[0] + ".json"
    if path:
        if not path[-1] == "/":
            path += "/"

        if path == ".":
            file_path = name    
        else:
            file_path = path + name
    
        if not Path(path).is_dir():
            Path(path).mkdir()
    else:
        file_path = name
        
    with open(file_path, "w") as f:
        dump(credentials_dict, f, indent = 4)

    