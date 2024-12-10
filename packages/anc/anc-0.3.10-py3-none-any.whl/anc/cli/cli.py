import click
from anc.version import __version__

from anc.cli import deployment
from anc.cli import dataset
from anc.cli.util import click_group

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.version_option(__version__, "-v", "--version")
@click_group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


#eployment.add_command(main)
dataset.add_command(main)

if __name__ == "__main__":
    main()
