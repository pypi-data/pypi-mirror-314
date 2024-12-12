import os
import subprocess

import click
from dotenv import load_dotenv

load_dotenv()

SERVICES = os.getenv("SYSTEMD_SERVICES", "")
if not SERVICES.strip():
    click.echo("⚠️  Warning: No services defined in the .env file. ⚠️")
    click.echo("Please define services in the .env file in the format:")
    click.echo("SYSTEMD_SERVICES=alias:service_name,alias2:service_name2")
    exit(1)
SERVICE_MAP = {
    s.split(":")[0]: s.split(":")[1] for s in SERVICES.split(",") if ":" in s
}
if not SERVICE_MAP:
    click.echo("⚠️  Warning: Services are not properly defined in the .env file. ⚠️")
    click.echo("Ensure each service entry follows the format:")
    click.echo("SYSTEMD_SERVICES=alias:service_name,alias2:service_name2")
    exit(1)


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Command failed: {e}")


@click.group()
def cli():
    """A cli tool to manage systemd services."""
    pass


@cli.command()
@click.argument("alias")
def restart(alias):
    """Restart a service."""
    if alias not in SERVICE_MAP:
        click.echo(f"Service alias '{alias}' not found in configuration.")
        return
    service_name = SERVICE_MAP[alias]
    click.echo(f"Restarting {service_name}...")
    run_command(["sudo", "systemctl", "restart", service_name])


@cli.command()
@click.argument("alias")
def status(alias):
    """Check the status of a service."""
    if alias not in SERVICE_MAP:
        click.echo(f"Service alias '{alias}' not found in configuration.")
        return
    service_name = SERVICE_MAP[alias]
    click.echo(f"Checking status of {service_name}...")
    run_command(["sudo", "systemctl", "status", service_name])


@cli.command()
@click.argument("alias")
def logs(alias):
    """Show the latest logs of a service."""
    if alias not in SERVICE_MAP:
        click.echo(f"Service alias '{alias}' not found in configuration.")
        return
    service_name = SERVICE_MAP[alias]
    click.echo(f"Fetching logs for {service_name}...")
    run_command(["sudo", "journalctl", "-u", service_name, "-n", "50", "--no-pager"])


@cli.command()
def list():
    """List all configured services."""
    click.echo("Configured services:")
    for alias, service in SERVICE_MAP.items():
        click.echo(f"  {alias}: {service}")


if __name__ == "__main__":
    cli()
