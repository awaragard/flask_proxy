#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os

import click
import yaml
from click_default_group import DefaultGroup
from flask import Flask

from flask_proxy import config, view, handler
from flask_proxy.resources import get_resource

config.init_logger(get_resource('logging_config.yml'))

@click.group(cls=DefaultGroup, default='run', default_if_no_args=True)
@click.help_option('-h', '--help')
def main():
    pass


@main.command(help='')
@click.option('-c', '--config-filename',
              default=get_resource('default_config.yml'),
              type=click.Path(exists=True))
def run(config_filename):
    start_server(config_filename)


def start_server(config_filename=None, **kwargs):
    opts = {}
    if config_filename:
        logging.getLogger().info("Reading proxy configuration from: {}".format(config_filename))
        with open(config_filename, 'r') as f:
            opts.update(yaml.safe_load(f))
    opts.update(kwargs)

    view.proxy_opts = config.ProxyOptions(**opts)
    view.logger = logging.getLogger('proxy')
    handler.register(view)

    # Init application
    logging.getLogger().info("Starting server")
    application = Flask(__name__)
    application.url_map.strict_slashes = False
    application.config.update(os.environ)
    application.register_blueprint(view.view)
    application.run(
        port=view.proxy_opts.port or 8080,
        debug=False,
        use_reloader=False,
        ssl_context='adhoc' if view.proxy_opts.protocol == "https" else None
    )


if __name__ == '__main__':
    main()
