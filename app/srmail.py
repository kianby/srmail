#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from clize import clize, run


@clize
def srmail_server(config_pathname):

    os.environ['CONFIG_PATHNAME'] = config_pathname

    from srmail import app
    app.run(host=app.config['app']['http']['host'],
            port=app.config['app']['http']['port'],
            debug=True, use_reloader=False)

if __name__ == '__main__':
    run(srmail_server)
