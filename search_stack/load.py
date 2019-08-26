#!/usr/bin/env python

import os
import yaml
from sqlalchemy import create_engine


class Load():
    def __init__(self):
        here = os.path.dirname( __file__ )
        target = os.path.abspath(os.path.join(here, '..'))

        with open(f'{target}/config/setup/setup.yml', 'r') as yml:
            self.setup = yaml.load(yml)

        self.conn = create_engine(self.setup['db_scheme'])
        connected = self.conn.has_table('variant_results')
        if not connected:
            raise OperationalError("Check database connection.")



