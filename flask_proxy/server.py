#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from flask import Flask

from ust_proxy.config import Config, Logging
from ust_proxy.resources import get_resource
from ust_proxy.view import system_view, proxy_view

# load root config
c = Config.from_yaml(get_resource("app.yaml"), merge_env=True)

# Load server level config
server_cfg = c.get_sub_config('server')

# Init the root logger and date format
log_cfg_path = get_resource(server_cfg.get_string('logging_cfg', required=True))
logs_root = server_cfg.get('logs_root', 'logs')
console_log_level = server_cfg.get('console_log_level', 'DEBUG')
Logging.init_logger(log_cfg_path, logs_root, console_log_level)
system_view.local_logs = logs_root

# Init application
application = Flask(__name__,
                    template_folder=get_resource('templates'),
                    static_folder=get_resource('static'))
application.url_map.strict_slashes = False
application.config.update(os.environ)

application.register_blueprint(system_view.system_view)
application.register_blueprint(proxy_view.proxy_view)

if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=server_cfg.get_int('port', 8080),
        debug=server_cfg.get_bool('debug', False),
        use_reloader=False
    )
