#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os

import click
from click_default_group import DefaultGroup
from flask import Flask
from qconf import QConfig

from flask_proxy import config, view, handler
from flask_proxy.resources import get_resource

# load root config
# Load server level config
# Init the root logger and date format
c = QConfig.from_yaml(get_resource("app.yml"))
server_cfg = c.get_sub_config('server')
config.init_logger(c['logging'])


@click.group(cls=DefaultGroup, default='run', default_if_no_args=True)
@click.help_option('-h', '--help')
def main():
    pass

@main.command(help='')
@click.option('-c', '--config-filename',
              default=get_resource('test_default.yml'),
              type=click.Path(exists=True))

def run(config_filename):

    view.proxy_opts = config.ProxyConfig(config_filename)
    view.logger = logging.getLogger('proxy')
    handler.register(view)

    # Init application
    application = Flask(__name__,
                        template_folder=get_resource('templates'),
                        static_folder=get_resource('static'))

    application.url_map.strict_slashes = False
    application.config.update(os.environ)
    application.register_blueprint(view.view)
    logging.getLogger().info("Starting server")
    application.run(
        host='0.0.0.0',
        port=server_cfg.get_int('port', 8080),
        debug=False,
        use_reloader=False,
        ssl_context='adhoc' if view.proxy_opts.protocol == "https" else None
    )

if __name__ == '__main__':
    main()
