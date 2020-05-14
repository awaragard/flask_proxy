#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from flask import Flask
from qconf import QConfig

from flask_proxy import config, view
from flask_proxy.resources import get_resource

# load root config
# Load server level config
# Init the root logger and date format
c = QConfig.from_yaml(get_resource("app.yaml"))
server_cfg = c.get_sub_config('server')
config.init_logger(c['logging'])

external_cfg_path = get_resource("test_default.yaml")
external_cfg = QConfig.from_yaml(external_cfg_path)
view.options = external_cfg
view.init_vcr()
# Init application
application = Flask(__name__,
                    template_folder=get_resource('templates'),
                    static_folder=get_resource('static'))
application.url_map.strict_slashes = False
application.config.update(os.environ)
application.register_blueprint(view.view)

if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=server_cfg.get_int('port', 8080),
        debug=False,
        use_reloader=False,
        ssl_context='adhoc'

    )


