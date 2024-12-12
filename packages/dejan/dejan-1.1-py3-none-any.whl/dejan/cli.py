import click
from dejan.apps.linkbert_app import run_linkbert
from dejan.apps.roo_app import run_roo
from dejan.apps.veczip_app import run_veczip
from dejan.apps.authority_app import run_authority

@click.group(help="""Dejan CLI for various tools.

Commands:

- authority: Fetch the authority metric for a given domain.
  Examples:
  1. Check authority by specifying the domain directly:
     dejan authority dejanmarketing.com
  2. Check authority by using the --domain option:
     dejan authority --domain dejanmarketing.com
  3. Prompt for domain if not provided:
     dejan authority

- roo: Fetch ROO data for a specific date or for the last 'n' days.
  Examples:
  1. Fetch ROO data for the most recent day (defaults to US mobile):
     dejan roo
  2. Fetch ROO data for the last 3 days in Australia on desktop:
     dejan roo 3 au desktop
  3. Fetch ROO data for a specific date (e.g., 2024-07-01) using US mobile:
     dejan roo 2024-07-01
  4. Fetch ROO data with arguments in any order:
     dejan roo au 3 desktop
  5. Prompt for missing arguments:
     dejan roo 2024-07-01 desktop

- linkbert: Run the LinkBERT CLI tool.
  Examples:
  1. Analyze text with default grouping strategy (phrase):
     dejan linkbert --text "LinkBERT is a model developed by Dejan."
  2. Analyze text with a specific grouping strategy:
     dejan linkbert --text "LinkBERT is a model developed by Dejan." --group token
  3. Prompt for text if not provided:
     dejan linkbert
  4. Use subtoken grouping strategy:
     dejan linkbert --text "LinkBERT is a model developed by Dejan." --group subtoken

- veczip: Compress embeddings using the veczip tool.
  Examples:
  1. Compress embeddings using default settings:
     dejan veczip input.csv output.npy
  2. Specify custom target dimensions:
     dejan veczip input.csv output.npy --target_dims 32
""")
def cli():
    """Dejan CLI for various tools."""
    pass

@cli.command()
@click.option('--text', default=None, help='The text to analyze.')
@click.option('--group', default="phrase", help='Grouping strategy (subtoken, token, phrase). Default is phrase.')
def linkbert(text, group):
    """Run LinkBERT to predict link tokens."""
    if not text:
        text = click.prompt("Enter text to analyze")
    
    run_linkbert(text, group)

@cli.command()
@click.argument('date_or_days', default="1", required=False)
@click.argument('region', default="us", required=False)
@click.argument('device', default="mobile", required=False)
def roo(date_or_days, region, device):
    """Fetch ROO data for a specific date or the last 'n' days."""
    run_roo(date_or_days, region, device)

@cli.command()
@click.argument('domain', required=False)
@click.option('--domain', '-d', help='The domain to analyze.')
def authority(domain):
    """Fetch the authority metric for a given domain."""
    if not domain:
        domain = click.prompt("Enter the domain to analyze")
    
    run_authority(domain)

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--target_dims', default=16, help="Number of dimensions to retain after compression. Default is 16.")
def veczip(input_file, output_file, target_dims):
    """
    Compress embeddings using veczip.

    Example:
    dejan veczip input.csv output.npy --target_dims 16
    """
    run_veczip(input_file, output_file, target_dims)

if __name__ == "__main__":
    cli()
