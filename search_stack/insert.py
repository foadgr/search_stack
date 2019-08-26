#!/usr/bin/env python

from search_stack.load import Load
import pandas as pd
import numpy as np
import requests
from zipfile import ZipFile, ZIP_STORED
import csv
from io import BytesIO
import re
import os


class Insert():
    def __init__(self):
        super().__init__()

        here = os.path.dirname( __file__ )
        self.target = os.path.abspath(os.path.join(here, '..'))

        self.uri = self.setup['download_uri']

        d = self.setup['dtypes']
        self.dtypes = {
            pd.to_datetime: d['dates'],
            pd.to_numeric: d['floats'],
            'excluded_chars': d['dates'] + d['floats']
        }

    def send_request(self):
        try:
            PARAMS = {'stream': True}
            res = requests.get(self.uri, params=PARAMS)
            if res.ok:
                return res
        except requests.ConnectionError as err:
            print(err.args[0])

    def retrieve_content(self):
        res = self.send_request()
        buffer = BytesIO(res.content)
        decomp_dat = ZipFile(buffer, compression=ZIP_STORED)
        fname = decomp_dat.namelist()[0]
        return decomp_dat.read(fname)

    @classmethod
    def row_reader(self, decompressed_file):
        dat = decompressed_file.decode('ISO-8859-1').splitlines()
        f = csv.reader(dat, delimiter='\t')
        return [row for row in f]

    @classmethod
    def fix_colnames(self, dfcols):
        sp, un = '\?|\(|\)|:|,|#|\.|%', '-|\s+|/|\n'
        def sub2(c):
            def sub1(c):
                return re.sub(un, '_', c.lower())
            return re.sub(sp, '', sub1(c))
        return [sub2(c) for c in dfcols]

    def cast(self, df):
        for k, v in self.dtypes.items():
            if k == 'excluded_chars':
                pat = r'^\s*$|^-$'
                func = lambda x: x.replace(pat, np.nan, regex=True)
                str_c = [col for col in df.columns if col not in v]
                df[str_c] = df[str_c].apply(func, axis=0)

            else:
                mapping = {
                    'func': k,
                    'downcast': 'float',
                    'errors': 'coerce'
                }

                try:
                    df[v] = df[v].apply(**mapping)
                except (KeyError, TypeError) as err:
                    print(err.args[0])
                    mapping.pop('downcast')
                    df[v] = df[v].apply(**mapping)
        return df

    def run(self):
        decompressed_file = self.retrieve_content()
        arr = self.row_reader(decompressed_file)
        df = pd.DataFrame(arr[1:], columns=arr[0])
        df.columns = self.fix_colnames(df.columns)
        return self.cast(df)

    def create_table(self):
        sql_file = open(f'{self.target}/config/setup/init.sql').read()
        self.conn.execute(sql_file)
        print(f"Created empty table: {self.conn.table_names()[0]}")
        return None

    def to_db(self, df=None):
        if df is None:
            df = self.run()
            print('Ran data.')
        mapping = {
            'name': self.conn.table_names()[0],
            'con': self.conn,
            'index': False,
            'if_exists': 'append'
        }

        df.to_sql(**mapping)
        print('Loaded data.')
        return None

if __name__ == "__main__":
    Insert().create_table()
    Insert().to_db()
