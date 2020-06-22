import click
from click_default_group import DefaultGroup

from flask_proxy.resources import get_resource
from flask_proxy.server import ProxyServer


@click.group(cls=DefaultGroup, default='run', default_if_no_args=True)
@click.help_option('-h', '--help')
def main():
    pass


@main.command(help='')
@click.option('-c', '--config-filename',
              default=get_resource('default_config.yml'),
              type=click.Path(exists=True))
def run(config_filename):
    ProxyServer.from_file(config_filename).start_sync()


if __name__ == '__main__':
    main()
