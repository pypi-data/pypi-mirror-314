#!/usr/bin/env python3
import click
from dataset_sh.subcmds.remote import remote_cli
from dataset_sh.subcmds.local import local_cli
from dataset_sh.subcmds.project import project_cli
from dataset_sh.subcmds.profile import profile_cli
from dataset_sh.subcmds.file import file_cli


@click.group(name='dataset.sh')
def dsh():
    pass


cli = dsh
cli.add_command(remote_cli)
cli.add_command(local_cli)
cli.add_command(file_cli)
cli.add_command(profile_cli)
cli.add_command(project_cli)

if __name__ == '__main__':  # pragma: no cover
    cli()
