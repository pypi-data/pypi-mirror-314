import click

@click.group()
def cli():
    """LS Infrastructure Management CLI"""
    pass

@cli.command()
def ping():
    """Simple ping command"""
    click.echo("pong")