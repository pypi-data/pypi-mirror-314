#!/usr/bin/env python3
from datetime import datetime
import re
import os
import sys
import time
import arrow
import shutil
from pathlib import Path
import json
import inquirer
import click
import subprocess
from . import cli
from .config import pass_config
from .config import Config


def get_sources(ctx, args, incomplete):
    config = Config()
    keys = list(config.sources.keys())
    if incomplete:
        keys = list(filter(lambda x: x.startswith(incomplete), keys))
    return keys


@cli.command()
@pass_config
def fetch(config):
    pass


def _get_files(config, shell, verbose=False, all=False):
    regex = config.get("regex", config.get("match", ".*"))
    if verbose:
        click.secho(f"Using regex '{regex}' to identify files.", fg="yellow")
    files = list(filter(bool, shell(["ls", "-tr", config["path"]])))
    for file in files:
        if all or re.findall(regex, file):
            yield file


def transfer(config, filename):
    destination = os.path.expanduser(config["destination"])
    source = f"{config['host']}:{config['path']}/{filename}"
    click.secho(f"Copying {source} to {destination}", fg="yellow")
    started = datetime.now()
    subprocess.run(["rsync", source, destination, "-arP"])
    seconds = (datetime.now() - started).total_seconds()
    click.secho(f"Success - done in {seconds}s", fg="green")


@cli.command(help="Choose specific file to download")
@click.argument("source", required=True, shell_complete=get_sources)
@click.option("--all", is_flag=True)
@pass_config
def choose(config, source, all):
    config.source = source
    with config.shell() as (config, shell):
        files = list(_get_files(config, shell, all=all))
        answer = inquirer.prompt(
            [inquirer.List("file", "Please choose:", choices=list(reversed(files)))]
        )
        if not answer:
            sys.exit(0)
        file = answer["file"]
        transfer(config, file)

def _generate_unique_filename(base_name, directory="."):
    """
    Generate a unique filename by appending a number to the base name if necessary.

    :param base_name: The starting base name of the file (e.g., "file").
    :param directory: The directory to check for existing files (default is the current directory).
    :return: A unique filename in the form 'base_name_number'.
    """
    counter = 1
    # Extract the file extension if it exists
    name, ext = os.path.splitext(base_name)
    
    # Check for unique filename
    unique_name = base_name
    while (directory / (unique_name  + ext)).exists():
        unique_name = f"{name}_{counter}{ext}"
        counter += 1
    
    return Path((directory / (unique_name + ext)))

@cli.command()
@click.argument("source", required=True)
@click.argument("host", required=True)
@click.argument("destination", required=True)
@click.argument("path", required=True)
@click.argument("match", required=True, default=".*")
@pass_config
def add(config, source, host, destination, match, path):

    configdir = Path(os.path.expanduser("~/.fetch_latest_file.d"))
    unique_file = _generate_unique_filename(source, configdir)
    unique_file.write_text(f"""[{source}]
host = {host}
path = {path}
regex = {match}
destination = {destination}
    """)

    click.secho(f"Successfully added:", fg="green")
    click.secho(f"\n{unique_file.absolute()}", fg='yellow')
    click.secho(unique_file.read_text(), fg='yellow')


@cli.command(name="all")
@pass_config
@click.option("-n", "--dryrun", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def fetch_all(config, dryrun, verbose):
    faileds = []
    for key in config.sources.keys():
        config.source = key
        try:
            _cmd_fetch(config, dryrun, verbose)
        except Exception as ex:
            faileds.append((config.source, ex))
    if faileds:
        for failed in faileds:
            click.secho(f"{failed[0]}: {str(failed[1])}", fg='red')
        sys.exit(-1)


@cli.command(name="fetch")
@pass_config
@click.argument("source", required=True, shell_complete=get_sources)
@click.option("-n", "--dryrun", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def cmd_fetch(config, source, dryrun, verbose):
    config.source = source
    _cmd_fetch(config, dryrun, verbose)

def _cmd_fetch(config, dryrun=False, verbose=False):
    with config.shell() as (config, shell):
        files = list(_get_files(config, shell, verbose=verbose))
        if not files:
            click.secho("No files found.")
            sys.exit(1)
        file = files[-1]
        if dryrun:
            click.secho(f"File {file} would be downloaded.", fg="green")
        else:
            transfer(config, file)


@cli.command()
def sample():
    click.secho(
        (
            "[name1]\n"
            "regex = *.dump.gz\n"
            "path = <remote path>\n"
            "host = <ssh host>\n"
            "destination = <here to put - a filename>\n"
        )
    )


@cli.command()
@click.option(
    "-x",
    "--execute",
    is_flag=True,
    help=("Execute the script to insert completion into users rc-file."),
)
def completion(execute):
    shell = os.environ["SHELL"].split("/")[-1]
    rc_file = Path(os.path.expanduser(f"~/.{shell}rc"))
    line = f'eval "$(_FETCH_COMPLETE={shell}_source fetch)"'
    if execute:
        content = rc_file.read_text().splitlines()
        if not list(
            filter(
                lambda x: line in x and not x.strip().startswith("#"),
                content,
            )
        ):
            content += [f"\n{line}"]
            click.secho(
                f"Inserted successfully\n{line}" "\n\nPlease restart you shell."
            )
            rc_file.write_text("\n".join(content))
        else:
            click.secho("Nothing done - already existed.")

    click.secho("\n\n" f"Insert into {rc_file}\n\n" f"echo 'line' >> {rc_file}" "\n\n")
