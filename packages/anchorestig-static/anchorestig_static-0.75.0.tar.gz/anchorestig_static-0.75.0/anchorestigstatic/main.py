import click
import argparse
import os
import subprocess
import signal

import itertools
import threading
import time
import sys

from .static import static_analysis, sync_policies, check_saf_installed
from .provision import install_cinc, install_train_plugin

@click.group()
def main():
    pass


@click.command()
@click.option('--username', '-u', help='Username for private registry')
@click.option('--password', '-p', help="Password for private registry")
@click.option('--url', '-r', help="URL for private registry")
@click.option('--aws-bucket', '-b', help="S3 upload. Specify bucket name")
@click.option('--account', '-a', help="Anchore STIG UI account. Required for S3 upload")
@click.option('--insecure', '-s', is_flag=True, default=False, help="Allow insecure registries or registries with custom certs")
@click.option('--profile', '-l', default="auto", help="Specify profile to run. Can be the name of an existing profile or the path to a custom profile")
@click.option('--input-file', '-i', help="Specify the path to a custom input file to run with a profile.")
@click.option('--sync', '-y', is_flag=True, default=False, help="Sync policies from Anchore")
@click.argument('image')
def static(username, password, url, insecure, image, aws_bucket, account, profile, input_file, sync):
    """Run static analysis"""
    if sync:
        sync_policies()
        print("Policies successfully downloaded.")
    check_saf_installed()
    if not input_file:
        input_file = "default"
    done = False
    def animate():
        print('Running STIG')
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')
    t = threading.Thread(target=animate)
    t.start()
    aws = aws_bucket
    static_analysis(username, password, url, insecure, image, aws, account, profile, input_file)
    done = True

@click.command()
def runtime():
    print("Please contact Anchore Sales for access to Anchore's Runtime STIG offering.")

@click.command()
def vm():
    print("Please contact Anchore Sales for access to Anchore's VM STIG offering.")

@click.command()
@click.option('--install', '-i', is_flag=True, default=False, help="Install the necessary version of CINC")
@click.option("--privileged", "-s", is_flag=True, default=False, help="Install CINC with sudo.")
@click.option("--plugin", "-p", is_flag=True, default=False, help="Install the CINC Train K8S Plugin")
def provision(install, privileged, plugin):
    if install:
        install_cinc(privileged)
    if plugin:
        install_train_plugin()

main.add_command(static)
main.add_command(runtime)
main.add_command(vm)
main.add_command(provision)


if __name__ == '__main__':
    main()
